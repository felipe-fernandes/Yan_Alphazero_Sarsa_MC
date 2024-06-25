from enum import Enum
from tqdm import tqdm
import json


class GAME_MOMENT(Enum):
    SECOS_1 = 1
    DADOS_1 = 2
    SECOS_2 = 3
    DADOS_2 = 4
    TABELA = 5
    FIM = 6


tqdm_obj = None

class VALUE_Table:
    def __init__(self, state) -> None:
        self.state = state
        
    
        self.create_actions_count_return(13)
        

    def create_actions_count_return(self, n):
        self.actions = [int(0)] * n
        self.actions_count = [int(0)] * n
        self.returns =  []
        for index in range(n):
            self.returns.append([])

    def toJson(self):
        serialized = '{"state":"' + str(self.state) + '", ' 
        serialized += '"actions": ['
        index = 0
        for action in self.actions:
            serialized += str(action)
            if index < len(self.actions) - 1:
                serialized += ","
            index += 1
        serialized += '], "actions_count": ['
        index = 0
        for count in self.actions_count:
            serialized += str(count)
            if index < len(self.actions_count) - 1:
                serialized += ","
            index += 1
        serialized += '],"returns":['
        outer_index = 0
        for action in self.returns:
            serialized += '['
            index = 0
            for reward in action:
                serialized += str(reward)
                if index < len(action) - 1:
                    serialized += ","
                index += 1
            serialized += ']'
            if outer_index < len(self.returns) - 1:
                serialized += ","
            outer_index += 1
        
        
        serialized += ']}'
          
        return serialized
    
    

