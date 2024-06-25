import numpy as np
from numpy import diff
from numpy import sum
from random import randint


class Yan:
    def __init__(self, args):
        # iniciar a coluna da desordem com -1 para indicar que as celulas estão vazias
        self.desordem = {"1": -1, "2": -1, "3": -1, "4": -1, "5": -1, "6": -1, "q": -1, "f": -1, "s+": -1, "s-": -1, "x+": -1, "x-": -1, "y": -1}
        self.yangame = "Yan_Game"
        self.rolls_left = 2
        self.dices = [0,0,0,0,0]
        self.new_dice = list()
        self.marcado_em = ""
        self.over_minimum = False
        self.is_ended = False
        self.game_play = []
        self.next_state = self.get_game_state()
        self.reward = 0
        self.valid_moves_items = []

        self.go_for_n_factor = args["go_for_n_factor"]
        self.go_for_q_factor = args["go_for_q_factor"]
        self.go_for_f_factor = args["go_for_f_factor"]
        self.go_for_s_factor = args["go_for_s_factor"]
        self.go_for_s__factor = args["go_for_s__factor"]
        self.go_for_y_factor = args["go_for_y_factor"]
        self.go_for_x_factor = args["go_for_x_factor"]
        self.go_for_x__factor = args["go_for_x__factor"]
        

    def check_consecutive(self, l):
        n = len(l) - 1
        return sum(diff(sorted(l)) == 1) >= n


    def roll_dice(self, n):
        # random.seed(42)

        rolls = list()
        for i in range(n):
            rolls.append(randint(1, 6))
        rolls.sort()
        self.game_play.append("você rolou:                          " + str(rolls))
        return rolls


    def get_game_state(self):
        state = [self.rolls_left]
        for die in self.dices:
            state.append(die)
        for item in self.desordem:
            if self.desordem[item] == -1:
                state.append(1)
            else:
                state.append(0)
        return state
        

    def set_state(self, state):
        self.is_ended = False
        self.rolls_left = state[0]
        index = 1
        for die in range(len(self.dices)):
            self.dices[die] = state[index]
            index += 1

        index = 6
        for item in self.desordem:
            if state[index] == 1:
                self.desordem[item] = -1
            else:
                self.desordem[item] = 0
            index += 1

        return self.get_game_state()


    def get_empty_cells(self, state):
        self.set_state(state)
        avaiable_list = {}
        for item in self.desordem:
            if self.desordem[item] == -1:
                avaiable_list[item] = self.desordem[item]
        return avaiable_list
    

    def get_number_of_actions(self, state):
        return 13


    def do_the_reroll(self, n_dices):
        dices_to_reroll = '{0:05b}'.format(int(n_dices))
        self.game_play.append("dados a serem rolados novamente:     " + dices_to_reroll)
        for index in range(len(str(dices_to_reroll))):
            if dices_to_reroll[index] == "1":
                self.dices[index] = self.roll_dice(1)[0]

        self.dices.sort()
        self.game_play.append("seus dados ficaram assim:            " + str(self.dices))
        # dice_set = set(self.dices)
        # n_single = len(dice_set)
        # return (6 - n_single) * 3
        return 0


    def reset(self):
        self.game_play = []
        self.game_play.append("Jogo iniciado")
        self.desordem = {"1": -1, "2": -1, "3": -1, "4": -1, "5": -1, "6": -1, "q": -1, "f": -1, "s+": -1, "s-": -1,
                         "x+": -1, "x-": -1,
                         "y": -1}
        self.dices = self.roll_dice(5)
        self.dices.sort()
        self.is_ended = False
        self.rolls_left = 2
        self.valid_moves_items = []
        # random.seed(42)

        initial_table = randint(1,8191)
        tabela = "{0:b}".format(initial_table)
        n_off_zeros = 13 - len(tabela)
        for i in range(n_off_zeros):
            tabela = "0" + tabela

        i = 0
        for item in self.desordem:
            if tabela[i] == "1":
                self.desordem[item] = -1
            else:
                self.desordem[item] = 0
            i += 1

        self.rolls_left = randint(0,2)

        return self.get_game_state()
    

    def get_initial_state(self):
        return self.reset()
    

    def get_valid_moves(self, state):
        self.valid_moves_items = []
        valid_action = []
        index = 0
        for item in self.desordem:
            if self.desordem[item] == -1:
                self.valid_moves_items.append(item)
                valid_action.append(1)
            else:
                valid_action.append(0)
            index += 1
        return valid_action


    def is_full(self):
        return ((self.dices[0] == self.dices[2] and self.dices[3] == self.dices[4]) or (
                        self.dices[0] == self.dices[1] and self.dices[2] == self.dices[4]))


    def set_cell_value(self, cell: str):

        self.is_ended = True
        self.game_play.append("você marcou                          " + str(self.dices) + " em " + cell)
        self.game_play.append("\n")
        
        # self.marcado_em = 
        # print(self.marcado_em)
        points = 0

        if cell == "1":
            points = self.dices.count(1)
            self.desordem["1"] = points
            return points
        
        elif cell == "2":
            points = self.dices.count(2) *2
            self.desordem["2"] = points
            return points
        
        elif cell == "3":
            points = self.dices.count(3) * 3
            self.desordem["3"] = points
            return points
        
        elif cell == "4":
            points = self.dices.count(4) * 4
            self.desordem["4"] = points
            return points
        
        elif cell == "5":
            points = self.dices.count(5) * 5
            self.desordem["5"] = points
            return points
        
        elif cell == "6":
            points = self.dices.count(6) * 6
            self.desordem["6"] = points
            return points
        
        elif cell == "y":
            if self.dices[0] == self.dices[4]:
                self.desordem["y"] = sum(self.dices) + 50
                return sum(self.dices) + 50
            else:
                self.desordem["y"] = 0
                return 0
            
        elif cell == "q":
            if self.dices[0] == self.dices[3]:
                self.desordem["q"] = sum(self.dices[:4]) + 30
                return sum(self.dices[:4]) + 30
            elif self.dices[1] == self.dices[4]:
                self.desordem["q"] = sum(self.dices[1:]) + 30
                return sum(self.dices[1:]) + 30
            else:
                self.desordem["q"] = 0
                return 0
            
        elif cell == "f":
            if self.is_full():
                self.desordem["f"] = sum(self.dices) + 20
                return sum(self.dices) + 20

            else:
                self.desordem["f"] = 0
                return 0
            
        elif cell == "s+":
            if self.check_consecutive(self.dices) and self.dices[0] == 2:
                self.desordem["s+"] = 60
                return 60
            else:
                self.desordem["s+"] = 0
                return 0
            
        elif cell == "s-":
            if self.check_consecutive( self.dices) and self.dices[0] == 1:
                self.desordem["s-"] = 50
                return 50
            else:
                self.desordem["s-"] = 0
                return 0
            
        elif cell == "x+":
            if (sum(self.dices) > self.desordem["x-"]) or self.desordem["x-"] == -1:
                self.desordem["x+"] = sum(self.dices)
                return sum(self.dices)
            else:
                self.desordem["x+"] = 0
            return 0
        
        elif cell == "x-":
            if (sum(self.dices) < self.desordem["x+"]) or self.desordem["x+"] == -1:
                self.desordem["x-"] = sum(self.dices)
                return sum(self.dices)
            else:
                self.desordem["x-"] = 0
            return 0
            

    def go_for_n(self, n):
        n_count = self.dices.count(n)
        if n_count == 5 or self.rolls_left == 0:
            self.rolls_left = 2
            reward = self.set_cell_value(str(n))
            self.dices = self.roll_dice(5)
            self.dices.sort()
            if n_count > 2:
                reward *= 2
            return reward
        else:
            for index in range(5):
                if self.dices[index] != n:
                    self.dices[index] = self.roll_dice(1)[0]

        self.rolls_left -= 1
        self.dices.sort()
        improve = self.dices.count(n) - n_count
        return 0


    def go_for_y(self):
        dices_count = []
        for n in range (1,7):
            dices_count.append(self.dices.count(n))
        if np.max(dices_count) > 4 or self.rolls_left == 0:
            self.rolls_left = 2
            reward = self.set_cell_value("y")
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward

        if dices_count.count(np.max(dices_count)) > 1:
            most_dices_indexs = []
            most_dices = None
            for index in range(len(dices_count)):
                if dices_count[index] == np.max(dices_count):
                    most_dices_indexs.append(index + 1)
            
            #checar qual dado manter dependendo da tabela
            for die in most_dices_indexs:
                if self.desordem[str(die)] == -1:
                    most_dices = die

            if most_dices == None:
                most_dices = most_dices_indexs[len(most_dices_indexs)-1]
        else:        
            most_dices = np.argmax(dices_count) + 1

        original_most_count_die = self.dices.count(most_dices)

        for index in range(5):
            if self.dices[index] != most_dices:
                self.dices[index] = self.roll_dice(1)[0]

        self.dices.sort()
        self.rolls_left -= 1
        final_most_count_die = self.dices.count(most_dices)
        improve = final_most_count_die - original_most_count_die
        return 0


    def go_for_q(self):
        dices_count = []
        for n in range (1,7):
            dices_count.append(self.dices.count(n))
        if np.max(dices_count) > 3 or self.rolls_left == 0:
            self.rolls_left = 2
            reward = self.set_cell_value("q")
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward

        if dices_count.count(np.max(dices_count)) > 1:
            most_dices_indexs = []
            most_dices = None
            for index in range(len(dices_count)):
                if dices_count[index] == np.max(dices_count):
                    most_dices_indexs.append(index + 1)
            
            #checar qual dado manter dependendo da tabela
            for die in most_dices_indexs:
                if self.desordem[str(die)] == -1:
                    most_dices = die

            if most_dices == None:
                most_dices = most_dices_indexs[len(most_dices_indexs)-1]
        else:        
            most_dices = np.argmax(dices_count) + 1

        original_most_count_die = self.dices.count(most_dices)

        for index in range(5):
            if self.dices[index] != most_dices:
                self.dices[index] = self.roll_dice(1)[0]

        self.dices.sort()
        self.rolls_left -= 1
        final_most_count_die = self.dices.count(most_dices)
        improve = final_most_count_die - original_most_count_die
        return 0


    def get_dices_for_f(self):
        dices_count = []
        least_dices = None
        most_dices = None


        for n in range (1,7):
            dices_count.append(self.dices.count(n))

        if dices_count.count(np.max(dices_count)) == 2:
            for index in range(len(dices_count)):
                if dices_count[index] == 1:
                    least_dices = (index + 1)

        elif dices_count.count(np.max(dices_count)) == 1:
            most_dices = np.argmax(dices_count) +1

        elif dices_count.count(np.max(dices_count)) > 2:
            most_dices = None
            most_dices_indexs = []
            for index in range(len(dices_count)):
                if dices_count[index] == np.max(dices_count):
                    most_dices_indexs.append(index + 1)
            
            #checar qual dado manter dependendo da tabela
            for die in most_dices_indexs:
                if self.desordem[str(die)] == -1:
                    most_dices = die

            if most_dices == None:
                most_dices = most_dices_indexs[len(most_dices_indexs)-1]

        return least_dices, most_dices


    def go_for_f(self):
        
        if self.is_full() or self.rolls_left == 0:
            self.rolls_left = 2
            reward = self.set_cell_value("f")
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward
        
        initial_least_dices, initial_most_dices = self.get_dices_for_f()

        initial_count = 0
        final_count = 0

        if initial_least_dices != None:
            initial_count = 1
            for index in range(5):
                if self.dices[index] == initial_least_dices:
                    self.dices[index] = self.roll_dice(1)[0]
            
        if initial_most_dices != None:
            initial_count = self.dices.count(initial_most_dices)
            for index in range(5):
                if self.dices[index] != initial_most_dices:
                    self.dices[index] = self.roll_dice(1)[0]
            
        final_least_dices, final_most_dices = self.get_dices_for_f()
        if initial_least_dices != None:
            if final_least_dices == None:
                final_count = 1
            else:
                final_count = 0
        else:
            if final_least_dices != None:
                final_count = 2 + (2 - initial_count)
            else:
                final_count = self.dices.count(final_most_dices) - initial_count

        self.dices.sort()
        self.rolls_left -= 1
        return 0


    def get_reroll_dices_s(self, witch_s):
        dices_count = []
        for n in range (1,7):
            dices_count.append(self.dices.count(n))
            
        reroll_dices = []

        if witch_s == "s+":
            for n in range(dices_count[0]):
                reroll_dices.append(1)
                
            for index in range(1, 6):
                for quant in range(dices_count[index] - 1):
                    reroll_dices.append(index + 1)

        else:
            for n in range(dices_count[5]):
                reroll_dices.append(6)

            for index in range(5):
                for quant in range(dices_count[index] - 1):
                    reroll_dices.append(index + 1)
       
        reroll_dices.sort()

        return reroll_dices


    def go_for_s(self, witch_s):
        
        if self.rolls_left == 0:
            self.rolls_left = 2
            reward = self.set_cell_value(witch_s)
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward
        
        if self.check_consecutive(self.dices) and self.dices[0] == 2 and witch_s == "s+":
            self.rolls_left = 2
            reward = self.set_cell_value("s+")
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward
        
        if self.check_consecutive(self.dices) and self.dices[0] == 1 and witch_s == "s-":
            self.rolls_left = 2
            reward = self.set_cell_value("s-")
            self.dices = self.roll_dice(5)
            self.dices.sort()
            return reward
        
        reroll_dices = self.get_reroll_dices_s(witch_s)
        original_n_dice_roled = len(reroll_dices)

        for index in range(5):
            if self.dices[index] in reroll_dices:
                reroll_dices = np.delete(reroll_dices, 0)
                self.dices[index] = self.roll_dice(1)[0]

        self.rolls_left -= 1
        self.dices.sort()
        final_n_dice_roled = len(self.get_reroll_dices_s(witch_s))
        improve = original_n_dice_roled - final_n_dice_roled
        return 0
    

    def get_next_state(self, state, action):
        if action == None:
            return (self.get_game_state(), 0, self.is_ended)
        self.set_state(state)
        action = int(action)
        self.reward = 0

        if action < 6:
            self.reward = self.go_for_n(action+1)*self.go_for_n_factor
        elif action == 6:
            self.reward = self.go_for_q()*self.go_for_q_factor
        elif action == 7:
            self.reward = self.go_for_f()*self.go_for_f_factor
        elif action == 8:
            self.reward = self.go_for_s("s+")*self.go_for_s_factor
        elif action == 9:
            self.reward = self.go_for_s("s-")*self.go_for_s__factor
        elif action == 10:
            self.rolls_left = 2
            self.reward = self.set_cell_value("x+")*self.go_for_x_factor
            # self.reward = 0
            self.dices = self.roll_dice(5)
            self.dices.sort()
        elif action == 11:
            self.rolls_left = 2
            self.reward = self.set_cell_value("x-")*self.go_for_x__factor
            # self.reward = 0
            self.dices = self.roll_dice(5)
            self.dices.sort()
        elif action == 12:
            self.reward = self.go_for_y()*self.go_for_y_factor
        else:
            breakpoint()
            print(action)
        return (self.get_game_state(), self.reward, self.is_ended)


    def get_value_and_terminated(self, state, action):
        if action == None:
            return (0, False)
        self.set_state(state)
        next_state, reward, is_ended = self.get_next_state(state, action)
        return reward, is_ended
    

    def get_total_score(self, state):
        self.set_state(state)
        self.score_values = list(self.desordem.values())
        self.total = sum(self.score_values)
        total_upper = sum(self.score_values[0:6])
        if total_upper >= 60:
            self.total += 30
        self.game_play.append("sua tabela ficou assim:              " + str(self.desordem))
        self.game_play.append("TOTAL:                               " + str(self.total))
        

        return self.total
    

    def get_encoded_state(self, state):

        encoded_state = []
        encoded_state.append(state[0]/2)
        for i in range(1,6):
            encoded_state.append(state[i]/6)
        encoded_state += state[6:]
        return encoded_state
    