from typing import Optional

import numpy as np

from battleship.logic.game import Field
import gymnasium as gym


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
                # "observation": gym.spaces.Box(low=0, high=1, shape=(2, self.size, self.size), dtype=np.int8),
                "observation": gym.spaces.MultiBinary(2 * self.size * self.size),
                "mask": gym.spaces.MultiBinary(n=size * size),
            }
        )

        # We can shoot at any playing field cell
        self.action_space = gym.spaces.Discrete(size * size)

        # Maps integer to field position
        self._action_to_position = lambda action: divmod(action, size)

    def _get_obs(self):
        unk = (self.view == 0)
        miss = np.array(self.view == 1)
        hit = np.array(self.view == 2)
        sank = (self.view == 3)

        return {
            # "observation": np.stack([unk, miss, hit, sank], axis=0).astype(np.float32),
            "observation": np.hstack([miss.flatten(), hit.flatten()]).astype(np.int8),
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
            # print(self.view)
            # print(action)
            # print(x, y)
            # print(self.legal_actions())
            # raise RuntimeError("Should not happen")
            reward = -1
            observation = self._get_obs()
            info = self._get_info()

            return observation, reward, False, False, info

        reward = 1
        status = self.field.check((x, y))

        match status:
            case 'miss':
                self.view[x, y] = 1
                reward = -0.15
            case 'hit':
                self.remaining -= 1
                self.view[x, y] = 2
                reward = 1
            case 'sank':
                self.remaining -= 1

                # Mark all cells of the last sunken ship in sank_mask
                last_sank_ship = self.field.sank[-1]
                for coord in last_sank_ship.status:
                    self.view[coord[0], coord[1]] = 3

                reward = 1

        # An environment is completed if and only if the agent has sunk all ships
        terminated = (self.remaining == 0)
        truncated = False

        if terminated:
            reward = 1

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