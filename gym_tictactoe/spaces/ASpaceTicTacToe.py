import gym
from gym import spaces
import numpy as np

class TicTacToeEncoding(gym.Space):
    def __init__(self, size = None):
        super(TicTacToeEncoding, self).__init__()

        self.size = size

    def sample(self):
        sample = np.zeros(self.size, dtype = int)
        sample[np.random.randint(0, self.size)] = 1

        return sample


    def contains(self, x): #Esto básicamente es comprobar si tiene el tamaño de self.size y si son todo 0 menos 1 número
        n_zeros = list(x).count(0)
        n_ones = list(x).count(1)

        if n_zeros + n_ones == self.size and n_ones == 1:
            return True
        else:
            return False

    def __repr__(self):
        return "TicTacToeEncoding({})".format(self.size)

    def __eq__(self,other):
        return self.size == other.size