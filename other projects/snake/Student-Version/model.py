import torch
import torch.nn as nn


class QNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)  # TODO
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)  # TODO
        self.fc3 = nn.Linear(hidden_dim, hidden_dim)  # TODO
        self.fc4 = nn.Linear(hidden_dim, output_dim)  # TODO
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.float()
        l1 = self.relu(self.fc1(x))
        l2 = self.relu(self.fc2(l1))  # TODO
        l3 = self.relu(self.fc3(l2))  # TODO
        l4 = self.fc4(l3)  # TODO
        return l4


def get_network_input(player, apple):
    proximity = player.get_proximity()
    x = torch.cat([torch.from_numpy(player.pos).double(), torch.from_numpy(apple.pos).double(),
                   torch.from_numpy(player.dir).double(), torch.tensor(proximity).double()])
    return x
