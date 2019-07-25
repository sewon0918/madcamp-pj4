# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""

from __future__ import print_function
import pickle
import numpy
#import torch
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from collections import OrderedDict
from policy_value_net_numpy import PolicyValueNetNumpy
from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                # location = [int(n, 8) for n in location.split(",")]
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 10, 10
    model_file = 'best_policy_10_10_5.model'
    # model_file = 'best_policy_8_8_5.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)
        # policyvaluenet = PolicyValueNet(board_width=width, board_height=height, model_file=model_file, use_gpu=False)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        try:
            policy_param = pickle.load(open(model_file, 'rb'))
        except:
            policy_param = pickle.load(open(model_file, 'rb'), encoding='bytes')  # To support python3
        # keys = ['conv1.weight', 'conv1.bias', 'conv2.weight', 'conv2.bias', 'conv3.weight', 'conv3.bias'
        #     , 'act_conv1.weight', 'act_conv1.bias', 'act_fc1.weight', 'act_fc1.bias'
        #     , 'val_conv1.weight', 'val_conv1.bias', 'val_fc1.weight', 'val_fc1.bias', 'val_fc2.weight',
        #         'val_fc2.bias']
        # param_pytorch = OrderedDict()
        # for key, value in zip(keys, policy_param):
        #     if 'fc' in key and 'weight' in key:
        #         param_pytorch[key] = torch.FloatTensor(value.T)
        #     elif 'conv' in key and 'weight' in key:
        #         param_pytorch[key] = torch.FloatTensor(value[:, :, ::-1, ::-1].copy())
        #     else:
        #         param_pytorch[key] = torch.FloatTensor(value)
        best_policy = PolicyValueNetNumpy(width, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
