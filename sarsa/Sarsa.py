import numpy as np
from tqdm import trange
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Yan_Game import Yan


class SARSA_Learning:


    def __init__(self,env:Yan, num_episodes):
        self.env=env
        self.record_reward = float('-inf')
        self.sum_reward = 0
        self.best_game = list()
        self.best_episode = 0

        #Defining the different parameters
        self.initial_epsilon = 0.9
        self.epsilon = 0.9
        self.total_episodes = num_episodes
        self.max_steps = 10000
        self.initial_alpha = 1.0
        self.alpha = 0.999999999
        self.gamma = 1

        self.Q = {"estado": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]}
        self.state_action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def get_action_for_input(self):
        state = input()
        print(self.choose_action(state))


    #Function to choose the next action
    def choose_action(self, state):
        action=0
        if np.random.uniform(0, 1) < self.epsilon or np.max(self.Q[str(state)]) == 0:
            action = np.random.choice(self.env.get_valid_actions(state))            
            
        else:
            if action >= self.env.get_number_of_actions(state):
                breakpoint()
            action = np.argmax(self.Q[str(state)])
   
        return action

    #Function to learn the Q-value
    def update(self, state, state2, reward, action, action2):
        state = str(state)
        state2 = str(state2)
        predict = self.Q[state][action]
        target = reward + self.gamma * self.Q[state2] [action2]
        self.Q[state] [action] = int(self.Q[state] [action] + self.alpha * (target - predict))
        # if np.max(self.Q[state]) != 0:
        #     self.save_q_state(self.Q[state])

    def edit_state(self, state):
        state = str(state)
        if state not in self.Q:
            self.Q[state] = self.state_action.copy()
        return self.Q[state]
        
            

    def start_training(self):
        reward=0

        for episode in trange(self.total_episodes):
            t = 0
            state1 = self.env.reset()
            self.sum_reward = 0
            self.edit_state(state1)
            action1 = self.choose_action(state1)
            while t < self.max_steps:

                state2, reward, done = self.env.get_next_state(state=state1, action=action1)
                self.edit_state(state2)

                # if reward < 0:
                self.sum_reward += reward


                if self.sum_reward > self.record_reward:

                    self.record_reward = self.sum_reward
                    self.best_episode = episode
                    self.best_table = self.env.desordem
                    
                #Choosing the next action
                if not env.check_ended(state2):
                    action2 = self.choose_action(state2)
                    self.update(state1, state2, reward, action1, action2)

                state1 = state2
                action1 = action2
                
                t += 1
                reward += 1
                #If at the end of learning process
                if env.check_ended(state2):
                    # k = self.alpha *  self.total_episodes
                    total_episode_percentage = episode/ (self.total_episodes * 0.7)
                    real_percentage = episode/ (self.total_episodes)
                    self.epsilon = self.initial_epsilon * (1-total_episode_percentage)
                    
                    # self.alpha = 1.0-real_percentage
                    self.best_game = list()
                    break
        
env = Yan()
sarsa = SARSA_Learning(env, 10000)
sarsa.start_training()

print(f"Record: {sarsa.record_reward}")
print(f"episódio: {sarsa.best_episode}")
print(f"Tabela: {sarsa.best_table}")
sarsa.epsilon = 0.0

def autoplay(env:Yan, sarsa:SARSA_Learning):
    total_reward = 0
    yangame = env
    state = yangame.get_initial_state()
    while not yangame.check_ended(state):
        if str(state) in sarsa.Q:
            action = sarsa.choose_action(state)
        else:
            action = np.random.choice(yangame.get_valid_actions(state))
        state2, reward, done = yangame.get_next_state(state=state, action=action)
        total_reward += reward
        state = state2
    
    return total_reward

avg_rewards = 0
sum_rewards = 0

for i in trange(1000):
    sum_rewards += autoplay(env=env, sarsa=sarsa)
    avg_rewards = sum_rewards/(i+1)

print(avg_rewards)