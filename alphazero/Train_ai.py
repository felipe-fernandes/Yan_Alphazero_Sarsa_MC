from numpy import diff
from numpy import sum
from random import randint
import json
import torch
from tqdm import trange
from Yan_Train_Game import Yan
from Models_Params import Models_Params
import jsonpickle
from Neuronet import Neuronet
from Alphazero import Alphazero


model_version = "v20"
filename = "modelsparams.json"


game_params = {
    "go_for_n_factor": 1,
    "go_for_q_factor": 1,
    "go_for_f_factor": 1,
    "go_for_s_factor": 1,
    "go_for_s__factor": 1,
    "go_for_y_factor": 1,
    "go_for_x_factor": 0,
    "go_for_x__factor": 0
}

game = Yan(args=game_params)


model = Neuronet(game, 4, 248)


saved_models_param_dict = {}
try:
    with open(filename) as json_file:
            jsonObj = json.load(json_file)
            unpickled = jsonpickle.decode(jsonObj)
    saved_models_param_dict = unpickled
except:
     pass




args = {
    
    'C': 2,
    'num_searches': 50,
    'num_iterations': 100,
    'num_selfPlay_iterations': 500,
    'num_epochs': 10,
    'batch_size': 128,
    'model_version': model_version
}

saved_params = Models_Params(
    args=args, 
    version=model_version, 
    policy_loss="cross_entropy", 
    value_loss="mse_loss",
    optim="Adam",
    lr=0.0001,
    game_params=game_params,
    mean_score=0.1
    ) 

saved_models_param_dict[model_version] = saved_params
pickled = jsonpickle.encode(saved_models_param_dict, unpicklable=False)

with open(filename, "w") as outfile:
    json.dump(pickled, outfile)


optimizer = torch.optim.Adam(model.parameters(), lr=saved_params.lr)

alphaZero = Alphazero(model, optimizer, game, args)
alphaZero.learn()

