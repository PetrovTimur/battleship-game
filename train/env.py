from typing import Optional

import numpy as np

from battleship.logic.game import Field
import gymnasium as gym


class TestBattleshipEnv:
    def __init__(self, size=10):
        self.size = size
        self.n_actions = size * size
        self.reset()

    def reset(self):
        self.field = Field()
        self.field.auto_place()
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


class BattleshipEnv(gym.Env):
    def __init__(self, size: int = 10):
        # The size of the playing field
        self.size = size

        self.field = None
        self.view = None
        self.remaining = None

        # The whole playing field
        self.observation_space = gym.spaces.Dict(
            {
                "observation": gym.spaces.Box(low=0, high=1, shape=(4, self.size, self.size), dtype=np.float32),
                "mask": gym.spaces.Box(low=0, high=1, shape=(self.size * self.size,), dtype=bool),
            }
        )

        # We can shoot at any playing field cell
        self.action_space = gym.spaces.Discrete(size * size)

        # Maps integer to field position
        self._action_to_position = lambda action: divmod(action, size)

    def _get_obs(self):
        unk = (self.view == 0)
        miss = (self.view == 1)
        hit = (self.view == 2)
        sank = (self.view == 3)

        return {
            "observation": np.stack([unk, miss, hit, sank], axis=0).astype(np.float32),
            "mask": self.legal_actions().astype(np.bool_),
        }

    def _get_info(self):
        return {
            "remaining": self.remaining,
        }

    def legal_actions(self):
        # return np.array([i for i,v in enumerate(self.view.flat) if v==0], dtype=np.int8)
        return np.array((self.view.flat == 0), dtype=np.int8)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)

        self.field = Field()
        self.field.auto_place()
        self.view = np.zeros((self.size, self.size), dtype=np.int8)
        # self.remaining = len(self.field.ships)
        self.remaining = sum(s.size for s in self.field.ships)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        # Map the action to field cell
        x, y = self._action_to_position(action)

        # Process shot
        if self.view[x, y] != 0:
            print(self.view)
            print(action)
            print(x, y)
            print(self.legal_actions())
            raise RuntimeError("Should not happen")

        reward = 0
        status = self.field.check((x, y))

        match status:
            case 'miss':
                self.view[x, y] = 1
                reward = -1
            case 'hit':
                self.remaining -= 1
                self.view[x, y] = 2
                reward = 5
            case 'sank':
                self.remaining -= 1

                # Mark all cells of the last sunken ship in sank_mask
                last_sank_ship = self.field.sank[-1]
                for coord in last_sank_ship.status:
                    self.view[coord[0], coord[1]] = 3

                reward = 10

        # An environment is completed if and only if the agent has sunk all ships
        terminated = (self.remaining == 0)
        truncated = False

        if terminated:
            reward = 100

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info


def main():
    env = BattleshipEnv()
    env.reset()
    print(*env.field.cells, sep='\n')
    print(env.remaining)
    print()


if __name__ == "__main__":
    main()