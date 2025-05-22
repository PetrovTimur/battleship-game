from torch import nn

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