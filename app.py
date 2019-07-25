from __future__ import print_function
import sys
import pickle
import numpy
#import torch
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from collections import OrderedDict
from policy_value_net_numpy import PolicyValueNetNumpy


# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras


input_from_app = sys.argv[1:]
model_file = './Omok/pj4/best_policy_10_10_5.model'
n = 5
height = width = 10

def parse(inputs):
    p1list = inputs[0].split(',')
    for i in range(len(p1list)):
        p1list[i] = int(p1list[i])
    p2list = inputs[1].split(',')
    for i in range(len(p2list)):
        p2list[i] = int(p2list[i])
    return (p1list, p2list)

def makemap(input1, input2):
    result = Board(width = width, height = height, n_in_row = n)
    result.init_board(start_player = 0)
    for i in range(len(input1)):
        result.states[input1[i]] = 1
        result.availables.remove(input1[i])
    for j in range(len(input2)):
        result.states[input2[j]] = 2
        result.availables.remove(input2[j])
    result.current_player = 1
    return result

parsed_input1, parsed_input2= parse(input_from_app)
board = makemap(parsed_input1, parsed_input2)

try:
    policy_param = pickle.load(open(model_file, 'rb'))

except:
    policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')  # To support python3

best_policy = PolicyValueNetNumpy(width, height, policy_param)
mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)  # set larger n_playout for better performance
print(mcts_player.get_action(board))
sys.stdout.flush()