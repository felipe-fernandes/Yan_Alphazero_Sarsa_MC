import numpy as np
from numpy import diff
from numpy import sum
from random import randint

import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Yan_Game import Yan
import torch
from tqdm import trange


from Yan_Game  import Yan
from Neuronet import Neuronet
from Models_Params import Models_Params

filename = "modelsparams.json"
version = "v20"


saved_models_param_dict = {}

# with open(filename) as json_file:
#         jsonObj = json.load(json_file)
#         unpickled = jsonpickle.decode(jsonObj)
# saved_models_param_dict = unpickled


def autoplay(model_version):
    yangame = Yan()
    state = yangame.get_initial_state()
    while True:
        valid_moves = yangame.get_valid_moves(state)
        encoded_state = yangame.get_encoded_state(state)
        rerols_left = state[0]
        dice = state[1:6]
        table = state[7:]
        
        tensor_state = torch.tensor(encoded_state).unsqueeze(0).float()

        model = Neuronet(yangame, 4, 248)

        model.load_state_dict(torch.load(model_version))
        model.eval()
        with torch.inference_mode():
            policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1)
        policy = policy.squeeze(0).numpy()

        valid_policy = policy * valid_moves

        input = np.argmax(valid_policy)

        user_input = str(input)
        action = input
        state = yangame.get_next_state(state, action)[0]
        if yangame.check_ended(state):
            return yangame.get_total_score(state)


def test_model(version):
    number_of_games = 1000
    model_version = f"alphazero/models/model_{version}.pt"
    media = 0
    sum_score = 0
    for i in trange(number_of_games):
        sum_score += autoplay(model_version)
        media = sum_score/(i+1)
    print(f"model: {model_version} média: {media}")

    # current_model_params = saved_models_param_dict[version]
    # updated_model_params = Models_Params(
    #      mean_score=media,
    #      args=current_model_params["params"],
    #      version=version,
    #      value_loss=current_model_params["value_loss"],
    #      policy_loss=current_model_params["policy_loss"],
    #      optim=current_model_params["optim"],
    #      lr=current_model_params["lr"],
    #      game_params=current_model_params["game_params"]
    # )
    # saved_models_param_dict[version] = updated_model_params

    # pickled = jsonpickle.encode(saved_models_param_dict, unpicklable=False, use_decimal=True)
    # with open(filename, "w") as outfile:
    #     json.dump(pickled, outfile)

test_model(version)