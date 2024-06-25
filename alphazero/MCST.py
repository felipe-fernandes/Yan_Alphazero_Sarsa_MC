import numpy as np
from numpy import diff
from numpy import sum
from random import randint
import math

import torch
from Yan_Train_Game import Yan

class Node:
    def __init__(self, game:Yan, args, state, parent=None, action_taken=None, prior=0):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior
        
        self.children = []
        
        self.visit_count = 0
        self.value_sum = 0
        
    def is_fully_expanded(self):
        return len(self.children) > 0
    
    def select(self):
        best_child = None
        best_ucb = -np.inf
        
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
                
        return best_child
    
    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior
    
    def expand(self, policy):
        child = None
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()
                child_state, child_reward, child_terminated = self.game.get_next_state(child_state, action)

                child = Node(self.game, self.args, child_state, self, action, prob)
                self.children.append(child)
        if child == None:
            breakpoint()
        return child
    
            
    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1
        
        # value = self.game.reward
        if self.parent is not None:
            self.parent.backpropagate(value)  


class MCTS:
    def __init__(self, game:Yan, args, model):
        self.game = game
        self.args = args
        self.model = model

    @torch.no_grad() 
    def search(self, state):
        root = Node(self.game, self.args, state)
        
        for search in range(self.args['num_searches']):
            node = root
            
            while node.is_fully_expanded():
                node = node.select()
                
            state, value, is_terminal = self.game.get_next_state(node.state, node.action_taken)
            
            if not is_terminal:
                tensor = torch.tensor(self.game.get_encoded_state(node.state)).unsqueeze(0)
                policy_init, value = self.model(
                    tensor.float()
                )   
                
                if np.isnan(policy_init[0][0]):
                    breakpoint()
                policy = torch.softmax(policy_init, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.game.get_valid_moves(node.state)
                policy *= valid_moves
                sum_policy = np.sum(policy)
                if sum_policy != 0:
                    policy = policy/sum_policy
                    node.expand(policy)

                # if np.isnan(out_policy[0]):
                #     out_policy = torch.softmax(policy_init, axis=1).squeeze(0).cpu().numpy()
                #     out_policy *= valid_moves
                # else:
                #     breakpoint()
                value = value.item()
                

            node.backpropagate(value)    
            
            
        # action_probs = self.game.get_valid_moves(state)
        action_probs = np.zeros(13)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        if np.sum(action_probs) != 0:
            action_probs /= np.sum(action_probs)
        if np.isnan(action_probs[0]):
            breakpoint()
        return action_probs
        
        
        