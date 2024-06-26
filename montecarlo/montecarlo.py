import logging
import numpy as np
import json
import time
from Node import VALUE_Table
# from loadjson import LOAD_Json
from datetime import datetime
from tqdm import tqdm
from tqdm import trange

import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Yan_Game import Yan



class Monte_carlo:


    def __init__(self,env:Yan):
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='yan-monte-carlo-test.log', encoding='utf-8', level=logging.DEBUG)

        self.env=env
        # self.filename = "yan-monte-carlo-13-actions-3.json"
        self.filename = "monte-carlo-test.json"

        self.initial_epsilon = 0.9
        self.epsilon = 0.9
        self.record_reward = float('-inf')
        self.sum_reward = 0
        self.best_game = np.empty(100, dtype=object)
        self.best_episode = 0
        self.next_state = ""
        self.full_value_table = {}
        # json_load = LOAD_Json(filename=self.filename)
        # self.full_value_table = json_load.get_unpickled()
        self.is_training = True


    # Define a random policy for the sake of demonstration
    def random_policy(self, state):
        if not self.is_training:
            return np.argmax(self.full_value_table[str(state)].actions)
        is_random = True
        self.edit_state(state)
        # action=0
        number_of_possible_actions = len(self.env.get_valid_actions(state))
        action = np.random.choice(self.env.get_valid_actions(state))            
        state = str(state)
        
        if np.random.uniform(0, 1) > self.epsilon:
            is_random = False
            arg_max = np.argmax(self.full_value_table[state].actions)
            arg_min = np.argmin(self.full_value_table[state].actions_count)
            # env.game_play.append("action values:                       " + str(self.full_value_table[state].actions))
            # env.game_play.append("action count:                        " + str(self.full_value_table[state].actions_count))
            if np.max(self.full_value_table[state].actions) != 0 and len(set(self.full_value_table[state].actions)) > 1:
                if 0 in self.full_value_table[state].actions_count and arg_min < number_of_possible_actions:
                    env.game_play.append("ação não explorada                " + str(arg_min))
                    action = arg_min
                else:
                    env.game_play.append("ação mais valiosa                 " + str(arg_max))
                    action = arg_max
        
        if is_random:
            env.game_play.append("ação aleatória" + str(action))
        self.full_value_table[state].actions_count[action] += 1
        # if action > number_of_possible_actions -1:
        #     breakpoint()
        return action


    def edit_state(self, state):
        state = str(state)
        v_table_item = VALUE_Table(state=state)

        if state not in self.full_value_table:
            self.full_value_table[v_table_item.state] = v_table_item
        return v_table_item


    # Monte Carlo Policy Evaluation function
    def monte_carlo_policy_evaluation(self, policy, env:Yan, num_episodes, gamma=1.0):

        value_table = self.full_value_table
        # self.edit_state(value_table)
        

        
        # returns = {state: [] for state in range(len(self.VT))}
        for _ in trange(num_episodes):
            # for i in range(1):
                # print("episodio               ", _)
            
            state = env.reset()
            sum_reward = 0
            episode = []
            # Generate an episode
            while True:
                action = policy(state = state)
                self.next_state, reward, terminal = env.get_next_state(state, action)
                sum_reward += reward
                if sum_reward > self.record_reward:
                    self.record_reward = sum_reward
                    self.best_episode = _                
                    for i in range(10):
                        self.logger.debug("Episodio:                %s", _)
                    self.logger.debug("record_reward:               %s", self.record_reward)
                    self.logger.debug("best_episode:                %s", self.best_episode)

                    for item in env.game_play:
                        self.logger.debug(item)

                # next_state = str(self.next_state)
                self.edit_state(state)
                if state == "":
                    breakpoint()
                episode.append((state, action, reward))
                if self.env.check_ended(self.next_state):
                    break
                state = self.next_state

            # Calculate the return and update the value table
            G = 0
            for state, action, reward in reversed(episode):
                state = str(state)
                G = int(gamma * G + reward)
                # self.edit_state(state)
                self.full_value_table[state].returns[action].append(G)
                if len(self.full_value_table[state].returns[action]) > 1000:
                    self.full_value_table[state].returns[action].pop(0)
                # self.returns[state] = [self.returns[state],G]
                self.full_value_table[state].actions[action] = int(np.mean(self.full_value_table[state].returns[action]))
                a = 1

            
            total_episode_percentage = _ / (num_episodes * 0.7)
            self.epsilon = self.initial_epsilon * (1-total_episode_percentage)

        self.is_training = False
        return value_table



# Define the number of episodes for MC evaluation
num_episodes = 100000

env = Yan()
V = Monte_carlo(env)
value_table_V = V.monte_carlo_policy_evaluation(policy=V.random_policy, env=env, num_episodes=num_episodes)
print("")
json_dict = tqdm(value_table_V)
json_dict.set_description("Dumping game to: " + V.filename)
def json_encoder(obj):
    if isinstance(obj, tqdm):
        return obj.iterable
    if isinstance(obj, VALUE_Table):
        json_dict.update(1)
        return_obj = obj.toJson()
        return return_obj
with open(V.filename, "w") as outfile:
    json.dump(json_dict, outfile, default=json_encoder)



def autoplay(env:Yan, mc:Monte_carlo):
    total_reward = 0
    yangame = env
    mc.is_training = False
    state = yangame.get_initial_state()
    while not yangame.check_ended(state):
        if str(state) in mc.full_value_table:
            action = mc.random_policy(state)
        else:
            action = np.random.choice(yangame.get_valid_actions(state))
        state2, reward, done = yangame.get_next_state(state=state, action=action)
        total_reward += reward
        state = state2
    
    return total_reward

avg_rewards = 0
sum_rewards = 0

for i in trange(1000):
    sum_rewards += autoplay(env=env, mc=V)
    avg_rewards = sum_rewards/(i+1)

print(avg_rewards)