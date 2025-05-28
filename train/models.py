from torch import nn
import torch
import torch.nn.init as init

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
            nn.Linear(64 * 5 * 5, 256),  # Input is 64*5*5 = 1600
            nn.ReLU(),
            nn.Linear(256, n_actions)  # Output layer, no activation for Q-values
        )

    def forward(self, x):
        x = self.conv(x)
        # print(x.shape, x)
        # x = x.view(x.size(0), -1)
        x = x.flatten(start_dim=1)
        # print(x.shape, x)
        return self.head(x)

class CNN(nn.Module):
    def __init__(self, in_channels=4, n_actions=100):
        super().__init__()

        self.conv = nn.Sequential(
            nn.ZeroPad2d(2),
            nn.Conv2d(in_channels=in_channels, out_channels=64, kernel_size=3, padding=0),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.Conv2d(64, 64, kernel_size=4, padding='same'),
            nn.ReLU()
        )
        self.head = nn.Sequential(
            nn.Linear(64 * 5 * 5, 256),  # Input is 64*5*5 = 1600
            nn.ReLU(),
            nn.Linear(256, n_actions)  # Output layer, no activation for Q-values
        )

    def forward(self, x):
        if x.dim() != 4:
            x = x.unsqueeze(0)

        x = self.conv(x)
        # print(x.shape, x)
        # x = x.view(x.size(0), -1)
        x = x.flatten(start_dim=1)
        # print(x.shape, x)
        x = self.head(x)

        # print(x.shape)
        # if x.shape[0] == 1:
        #     return x.squeeze()
        return x


class MLP(nn.Module):
    def __init__(self, in_channels=4, n_size=10, hidden_size=256, n_actions=100):
        super().__init__()

        self.flatten = nn.Flatten()

        self.linear = nn.Sequential(
            nn.Linear(in_features=in_channels * n_size * n_size, out_features=hidden_size),
            nn.Tanh(),
            nn.Linear(in_features=hidden_size, out_features=hidden_size),
            nn.Tanh(),
            nn.Linear(in_features=hidden_size, out_features=n_actions)
        )

        self.apply(self._orthogonal_init)

    def _orthogonal_init(self, m):
        if isinstance(m, nn.Linear):
            init.orthogonal_(m.weight)
            if m.bias is not None:
                init.zeros_(m.bias)

    def forward(self, x):
        # print('x shape ', x.shape)
        if x.dim() != 2:
            x = x.unsqueeze(0)

        if x.dtype != torch.float32:
            x = x.float()

        x = self.flatten(x)
        x = self.linear(x)

        # print('x out shape ', x.shape)
        return x