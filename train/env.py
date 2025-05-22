import numpy as np
from battleship.logic.game import Field


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
