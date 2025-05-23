import numpy as np
import matplotlib.pyplot as plt
import torch
from env import BattleshipEnv
from models import DQN


# Load trained model
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def evaluate(n_games=100):
    # Load model
    checkpoint_path = 'checkpoints/ppo_1.pt'
    env = BattleshipEnv()
    policy_net = DQN(n_actions=env.size * env.size).to(device)
    policy_net.load_state_dict(torch.load(checkpoint_path, map_location=device))
    policy_net.eval()

    moves_list = []
    for _ in range(n_games):
        obs, info = env.reset()
        state = torch.tensor(obs["observation"], dtype=torch.float32, device=device).unsqueeze(0)
        done = False
        moves = 0
        while not done:
            with torch.no_grad():
                q = policy_net(state)
                mask = torch.full_like(q, float('-inf'))
                legal_mask = torch.tensor(obs["mask"], dtype=torch.bool, device=device)
                mask[0, legal_mask] = 0
                action = (q + mask).argmax(1).item()
            obs2, _, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            if not done:
                state = torch.tensor(obs2["observation"], dtype=torch.float32, device=device).unsqueeze(0)
                obs = obs2
            moves += 1
        moves_list.append(moves)

    # Statistics
    avg_moves = np.mean(moves_list)
    min_moves = np.min(moves_list)
    max_moves = np.max(moves_list)
    print(f"Games: {n_games}, Avg moves: {avg_moves:.2f}, Min: {min_moves}, Max: {max_moves}")

    # Plots
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(moves_list, bins=range(min_moves, max_moves + 2), color='skyblue', edgecolor='black')
    ax1.set_title('Moves per Game (Histogram)')
    ax1.set_xlabel('Moves')
    ax1.set_ylabel('Frequency')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.boxplot(moves_list, vert=True)
    ax2.set_title('Moves per Game (Boxplot)')
    ax2.set_ylabel('Moves')

    ax3 = fig.add_subplot(gs[1, :])
    ax3.plot(moves_list, marker='.', linestyle='None', alpha=0.5, label='Moves per Game')
    ax3.set_ylim(bottom=30, top=100)
    window = 20
    if n_games >= window:
        running_avg = [np.mean(moves_list[max(0, i-window+1):i+1]) for i in range(len(moves_list))]
        ax3.plot(running_avg, color='red', linewidth=2, label=f'Running Avg (window={window})')
    ax3.set_title('Moves per Game (Line Plot)')
    ax3.set_xlabel('Game #')
    ax3.set_ylabel('Moves')
    ax3.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    evaluate(n_games=100)
