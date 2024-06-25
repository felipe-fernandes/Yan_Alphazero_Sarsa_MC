import numpy as np
from numpy import diff
from numpy import sum
from random import randint
from Yan_Train_Game import Yan
from MCST import MCTS
import random
import torch
from tqdm import trange

import torch.nn.functional as F


class Alphazero:
    def __init__(self, model, optimizer, game:Yan, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = MCTS(game, args, model)
        
    def selfPlay(self):
        memory = []
        # player = 1
        state = self.game.get_initial_state()
        
        while True:
            # neutral_state = self.game.change_perspective(state, player)
            action_probs = self.mcts.search(state)
            
            memory.append((state, action_probs))

            if np.sum(action_probs) == 0:
                # breakpoint()
                returnMemory = [(self.game.get_encoded_state(state), action_probs, 0)]
                return returnMemory
            
            action = np.random.choice(self.game.get_number_of_actions(state), p=action_probs)
            
            state, reward, terminal = self.game.get_next_state(state, action)
            
            value, is_terminal = self.game.get_value_and_terminated(state, action)
            
            if is_terminal:
                returnMemory = []
                for hist_state, hist_action_probs in memory:
                    hist_outcome = value
                    returnMemory.append((
                        self.game.get_encoded_state(hist_state),
                        hist_action_probs,
                        hist_outcome
                    ))
                return returnMemory
            
            # player = self.game.get_opponent(player)
                
    def train(self, memory):
        random.shuffle(memory)
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            sample = memory[batchIdx:min(len(memory) - 1, batchIdx + self.args['batch_size'])] 
            try:
                state, policy_targets, value_targets = zip(*sample)
                
                state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)
                
                state = torch.tensor(state, dtype=torch.float32)
                policy_targets = torch.tensor(policy_targets, dtype=torch.float32)
                value_targets = torch.tensor(value_targets, dtype=torch.float32)
                
                out_policy, out_value = self.model(state)
                
                policy_loss = F.cross_entropy(out_policy, policy_targets)
                value_loss = F.mse_loss(out_value, value_targets)
                loss = policy_loss + value_loss
                
                self.optimizer.zero_grad() # change to self.optimizer
                loss.backward()
                self.optimizer.step() # change to self.optimizer
            except:
                pass
    
    def learn(self):
        for iteration in trange(self.args['num_iterations']):
            memory = []
            
            self.model.eval()
            for selfPlay_iteration in range(self.args['num_selfPlay_iterations']):
                memory += self.selfPlay()
                
            self.model.train()
            for epoch in range(self.args['num_epochs']):
                self.train(memory)
            version = self.args['model_version']
            if (iteration + 1) == self.args['num_iterations']:
                torch.save(self.model.state_dict(), f"alphazero/models/model_{version}.pt")
                torch.save(self.optimizer.state_dict(), f"alphazero/models/optimizer_{version}.pt")