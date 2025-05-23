import torch
import numpy as np
import matplotlib.pyplot as plt
from env import BattleshipEnv
from models import DQN

# Load trained model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
checkpoint_path = 'checkpoints/ppo_1.pt'
env = BattleshipEnv()
policy_net = DQN(n_actions=env.size * env.size).to(device)
policy_net.load_state_dict(torch.load(checkpoint_path, map_location=device))
policy_net.eval()

print(sum(p.numel() for p in policy_net.parameters()))

obs, info = env.reset()
state = torch.tensor(obs["observation"], device=device).unsqueeze(0)
done = False
shot_order = np.zeros((env.size, env.size), dtype=int)
step = 1

while not done:
    with torch.no_grad():
        q = policy_net(state)
        mask = torch.full_like(q, float('-inf'))
        legal_mask = torch.tensor(obs["mask"], dtype=torch.bool, device=device)
        mask[0, legal_mask] = 0
        action = (q + mask).argmax(1).item()
    x, y = divmod(action, env.size)
    shot_order[x, y] = step
    step += 1
    obs2, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    if not done:
        state = torch.tensor(obs2["observation"], device=device).unsqueeze(0)
        obs = obs2

# Get ship positions
ship_mask = np.zeros((env.size, env.size), dtype=bool)
for ship in env.field.ships:
    for (x, y) in ship.status.keys():
        ship_mask[x, y] = True

# Visualization
plt.figure(figsize=(6,6))

background = np.zeros((env.size, env.size, 4), dtype=float)
background[:, :] = [0, 0.3, 1, 1]  # Blue
background[shot_order > 0] = [0, 0, 0, 1]  # Black for shot cells
plt.imshow(background, interpolation='none')

# Overlay ships in red
ship_overlay = np.zeros((*ship_mask.shape, 4))
ship_overlay[ship_mask] = [1, 0, 0, 0.5]  # Red with alpha=0.5
plt.imshow(ship_overlay, interpolation='none')

# Draw shot order numbers in every cell
for x in range(env.size):
    for y in range(env.size):
        plt.text(y, x, str(shot_order[x, y]), ha='center', va='center', color='white', fontsize=8)

plt.title('Order of Shots by DQN (Ships in Red)')
plt.axis('off')
plt.show()
