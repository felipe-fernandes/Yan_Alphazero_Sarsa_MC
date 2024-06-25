import numpy as np
from numpy import diff
from numpy import sum
from random import randint

import torch
import torch.nn as nn
import torch.nn.functional as F


class Neuronet(nn.Module):
    def __init__(self, game, num_resBlocks, num_hidden):
        super().__init__()
        self.startBlock = nn.Sequential(
            nn.Linear(in_features=19, out_features=num_hidden),
            nn.ReLU()
        )
        
        self.backBone = nn.ModuleList(
            [ResBlock(num_hidden) for i in range(num_resBlocks)]
        )
        
        self.policyHead = nn.Sequential(
            nn.Linear(in_features=num_hidden, out_features=num_hidden),
            # nn.BatchNorm1d(num_hidden),
            nn.ReLU(),
            nn.Linear(num_hidden, 13)
        )
        
        self.valueHead = nn.Sequential(
            nn.Linear(in_features=num_hidden, out_features=num_hidden),
            # nn.BatchNorm1d(num_hidden),
            nn.ReLU(),
            nn.Linear(num_hidden, 1),
            nn.Tanh()
        )
        
    def forward(self, x):
        x = self.startBlock(x)
        for resBlock in self.backBone:
            x = resBlock(x)
        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value
        
        
class ResBlock(nn.Module):
    def __init__(self, num_hidden):
        super().__init__()
        self.lin1 = nn.Linear(in_features=num_hidden, out_features=num_hidden)
        # self.bn1 = nn.BatchNorm1d(num_hidden)
        self.lin2 = nn.Linear(in_features=num_hidden, out_features=num_hidden)
        # self.bn2 = nn.BatchNorm1d(num_hidden)
        
    def forward(self, x):
        residual = x
        x = F.relu(self.lin1(x))
        x = self.lin2(x)
        x += residual
        x = F.relu(x)
        return x
        