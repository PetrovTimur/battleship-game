import math, random
from collections import deque, namedtuple
from itertools import count
import os

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from battleship.logic.game import Field

# device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Environment wrapper ---
class BattleshipEnv:
    def __init__(self, size=10):
        self.size = size
        self.n_actions = size * size
        self.reset()

    def reset(self):
        self.field = Field(); self.field.auto_place()
        self.view = np.zeros((self.size, self.size), dtype=np.int8)
        self.remaining = sum(s.size for s in self.field.ships)
        self.done = False
        # Track which cells are part of sunken ships
        self.sank_mask = np.zeros((self.size, self.size), dtype=np.bool_)
        return self._get_obs()

    def _get_obs(self):
        # one-hot channels: unknown(0), miss(1), hit(2), sunk(3)
        v = self.view
        # Channel 0: unknown
        ch0 = (v == 0)
        # Channel 1: miss
        ch1 = (v == 1)
        # Channel 2: hit (not sunk)
        ch2 = (v == 2) & (~self.sank_mask)
        # Channel 3: sunk
        ch3 = self.sank_mask
        return np.stack([ch0, ch1, ch2, ch3], axis=0).astype(np.float32)

    def step(self, action):
        if self.done:
            raise RuntimeError("Episode done – call reset()")
        x, y = divmod(action, self.size)
        if self.view[x, y] != 0:
            raise RuntimeError("Should not happen")
            # self.done = True
            # return self._get_obs(), -5.0, True
        res = self.field.check((x, y))
        if res in ('hit','sank'):
            self.view[x, y] = 2
            reward = 5.0 if res=='hit' else 10.0
            self.remaining -= 1
            if res == 'sank':
                # Mark all cells of the last sunken ship in sank_mask
                last_sank_ship = self.field.sank[-1]
                for coord in last_sank_ship.status:
                    self.sank_mask[coord[0], coord[1]] = True
        else:
            self.view[x, y] = 1
            reward = -1.0
        if self.remaining == 0:
            self.done = True
            reward += 100.0
        return self._get_obs(), reward, self.done

    def legal_actions(self):
        return [i for i,v in enumerate(self.view.flat) if v==0]


# --- DQN network ---
class DQN(nn.Module):
    def __init__(self, in_channels=4, n_actions=100):
        super().__init__()
        self.conv = nn.Sequential(
            nn.ZeroPad2d(2),
            nn.Conv2d(in_channels=4, out_channels=64, kernel_size=3, padding=0),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.Conv2d(64, 64, kernel_size=4, padding='same'),
            nn.ReLU()
        )
        self.head = nn.Sequential(
            nn.Linear(64 * 5 * 5, 128),  # Input is 64*5*5 = 1600
            nn.ReLU(),
            nn.Linear(128, n_actions)  # Output layer, no activation for Q-values
        )

    def forward(self, x):
        x = self.conv(x)
        return self.head(x.view(x.size(0), -1))


# --- Replay Buffer ---
Transition = namedtuple('Transition', ('state','action','next_state','reward'))
class ReplayMemory:
    def __init__(self, capacity):
        self.buf = deque(maxlen=capacity)
    def push(self, *args):
        self.buf.append(Transition(*args))
    def sample(self, bsize):
        return random.sample(self.buf, bsize)
    def __len__(self):
        return len(self.buf)

# --- Plotting ---
def plot(stats):
    plt.figure(1, figsize=(10, 8))
    plt.clf()
    plt.subplot(2, 2, 1)
    plt.title("Episode Reward")
    plt.plot(stats['rewards'])
    plt.subplot(2, 2, 2)
    plt.title("Loss")
    plt.plot(stats['losses'])
    plt.subplot(2, 2, 3)
    plt.title("Epsilon")
    plt.plot(stats['epsilons'])
    plt.subplot(2, 2, 4)
    plt.title("Avg Steps/Episode")
    plt.plot(stats['steps'])
    plt.tight_layout()
    plt.pause(0.001)

def main():
    # --- Hyperparams ---
    EPS_START, EPS_END, EPS_DECAY = 1.0, 0.05, 200000
    GAMMA = 0.99
    BATCH_SIZE = 64
    LR = 2e-5
    TARGET_UPDATE = 100
    MEM_CAP = 10000
    NUM_EPISODES = 5000
    TARGET_UPDATE_STEPS = 1000

    # --- Epsilon schedule ---
    def epsilon_by_frame(frame):
        return EPS_END + (EPS_START - EPS_END) * math.exp(-1. * frame / EPS_DECAY)

    # --- Action selection ---
    def select_action(state, step_idx):
        eps = epsilon_by_frame(step_idx)
        if random.random() < eps:
            return torch.tensor([[env.legal_actions()[random.randrange(len(env.legal_actions()))]]],
                                device=device, dtype=torch.long)
        else:
            with torch.no_grad():
                # q = policy_net(state)
                # mask = torch.full_like(q, -(10 ** 5))
                # mask[0, env.legal_actions()] = 0
                # return (q + mask).argmax(1).view(1, 1)
                q = policy_net(state)
                legal = env.legal_actions()
                illegal = [i for i in range(q.size(1)) if i not in legal]
                q_clone = q.clone()
                q_clone[0, illegal] = -(10 ** 5)
                return q_clone.argmax(1).view(1, 1)

    # --- Optimization (Double DQN) ---
    def optimize():
        if len(memory) < BATCH_SIZE:
            return None
        trans = memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*trans))

        non_final_mask = torch.tensor([s is not None for s in batch.next_state],
                                      device=device, dtype=torch.bool)
        non_final_next = torch.cat([s for s in batch.next_state if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # current Q
        q_values = policy_net(state_batch).gather(1, action_batch)

        # Double DQN next Q
        next_actions = policy_net(non_final_next).argmax(1, keepdim=True)
        next_q = torch.zeros(BATCH_SIZE, device=device)
        # Calculate Q-values using target_net for actions selected by policy_net
        # Use .detach() to prevent gradients from flowing back through the target network
        # during the loss calculation for the policy network.
        next_q_values = target_net(non_final_next).gather(1, next_actions)
        next_q[non_final_mask] = next_q_values.squeeze().detach()  # <<< ADDED .detach() HERE

        # Compute the expected Q values
        expected = reward_batch + GAMMA * next_q
        # Compute Huber loss
        loss = F.smooth_l1_loss(q_values.squeeze(), expected)  # Use q_values.squeeze() to match shape
        optimizer.zero_grad()
        loss.backward()
        # Gradient clipping helps prevent exploding gradients
        nn.utils.clip_grad_norm_(policy_net.parameters(), 1.0)
        optimizer.step()
        return loss.item()

    env = BattleshipEnv()
    policy_net = DQN(n_actions=env.n_actions).to(device)
    target_net = DQN(n_actions=env.n_actions).to(device)

    # Load checkpoint if exists
    checkpoint_path = "dqn_battleship.pt"
    if os.path.exists(checkpoint_path):
        print(f"Loading checkpoint from {checkpoint_path}")
        policy_net.load_state_dict(torch.load(checkpoint_path, map_location=device))
        target_net.load_state_dict(policy_net.state_dict())
    else:
        target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    memory = ReplayMemory(MEM_CAP)

    stats = {'rewards':[], 'losses':[], 'epsilons':[], 'steps':[]}
    step_idx = 0

    for ep in range(1, NUM_EPISODES+1):
        obs = env.reset()
        state = torch.tensor(obs, device=device).unsqueeze(0)
        total_r, done = 0.0, False
        steps_this_ep = 0

        while not done:
            eps = epsilon_by_frame(step_idx)
            action = select_action(state, step_idx)
            step_idx += 1
            obs2, reward, done = env.step(action.item())
            total_r += reward
            r_t = torch.tensor([reward], device=device)

            next_state = None if done else torch.tensor(obs2, device=device).unsqueeze(0)
            memory.push(state, action, next_state, r_t)
            state = next_state

            loss = optimize()
            if loss is not None:
                stats['losses'].append(loss)

            if step_idx % TARGET_UPDATE_STEPS == 0:
                target_net.load_state_dict(policy_net.state_dict())
                print(f"*** Updated Target Network at step {step_idx} ***")

            steps_this_ep += 1

        stats['rewards'].append(total_r)
        stats['epsilons'].append(epsilon_by_frame(step_idx))
        stats['steps'].append(steps_this_ep)
        
        # hard update
        if ep % TARGET_UPDATE == 0:
            torch.save(policy_net.state_dict(), "dqn_battleship.pt")

        # logging & plotting
        if ep % 50 == 0:
            avg_r = np.mean(stats['rewards'][-10:])
            avg_l = np.mean(stats['losses'][-50:]) if stats['losses'] else 0
            avg_s = np.mean(stats['steps'][-10:]) if stats['steps'] else 0
            print(f"Ep {ep:4d}  AvgR10={avg_r:.2f}  AvgL50={avg_l:.4f}  AvgSteps10={avg_s:.2f}")
            plot(stats)

    plt.ioff(); plt.show()
    # Save final model
    torch.save(policy_net.state_dict(), "dqn_battleship.pt")

if __name__ == "__main__":
    main()

