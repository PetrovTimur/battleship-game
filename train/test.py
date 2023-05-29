import copy
from random import randint
from battleship.logic.ai import random_ships_matrix, random_ships
from battleship.logic.game import Field
import matplotlib.pyplot as plt  # Added for plotting

def is_alive(field):
    # A bot is alive if any ship cells remain (>0)
    for row in field.cells:
        if any(cell > 0 for cell in row):
            return True
    return False

def shot(cells):
    coords = randint(0, 9), randint(0, 9)
    while cells[coords[0]][coords[1]] < 0:
        coords = randint(0, 9), randint(0, 9)

    return coords

def play_game():
    field = Field()
    field.cells = random_ships_matrix()
    # print(*field.cells, sep='\n')
    moves = 0
    while is_alive(field):
        target = shot(field.cells)
        field.check(target)
        moves += 1
    return moves

def main():
    num_games = 1000
    moves_list = []
    for _ in range(num_games):
        moves = play_game()
        moves_list.append(moves)
    print(f"Games played: {num_games}")
    print(f"Average moves: {sum(moves_list) / num_games:.2f}")
    print(f"Min moves: {min(moves_list)}")
    print(f"Max moves: {max(moves_list)}")

    # --- Plots ---
    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])

    # Histogram (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(moves_list, bins=range(min(moves_list), max(moves_list) + 2), color='skyblue', edgecolor='black')
    ax1.set_title('Moves per Game (Histogram)')
    ax1.set_xlabel('Moves')
    ax1.set_ylabel('Frequency')

    # Boxplot (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.boxplot(moves_list, vert=True)
    ax2.set_title('Moves per Game (Boxplot)')
    ax2.set_ylabel('Moves')

    # Line plot (bottom, spanning both columns)
    ax3 = fig.add_subplot(gs[1, :])
    ax3.plot(moves_list, marker='.', linestyle='-', alpha=0.5, label='Moves per Game')

    # Running average
    window = 50
    if len(moves_list) >= window:
        running_avg = [sum(moves_list[max(0, i-window+1):i+1]) / (i - max(0, i-window+1) + 1) for i in range(len(moves_list))]
        ax3.plot(running_avg, color='red', linewidth=2, label=f'Running Avg (window={window})')

    ax3.set_title('Moves per Game (Line Plot)')
    ax3.set_xlabel('Game #')
    ax3.set_ylabel('Moves')
    ax3.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
