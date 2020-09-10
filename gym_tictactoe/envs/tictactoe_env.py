import gym
from gym import spaces
from copy import copy
import random
from gym_tictactoe.spaces import TicTacToeEncoding #Este es el espacio que he creado a posta
import numpy as np

#Env template

class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, dim = 3):
        super(TicTacToeEnv, self).__init__()
        self.dim = dim #Esto te brinda la posibilidad de jugar a TicTacToe de más dimensiones, lo cual pues está curioso
        self.tablero = np.array([0]*self.dim**2)
        self.fichas = [-1, 1] #Lista con las posibles fichas
        self.ficha = 1

        #Hay que definir el observation y el action space
        self.action_space = TicTacToeEncoding(self.dim**2)

        #Para considerar el tablero y la ficha que le toca poner podemos hacer esto como una tupla de (tablero, ficha)
        #La ficha 0 --> -1 / 1 --> 1
        self.observation_space = spaces.Tuple((spaces.Box(low = -1, high = 1, shape = (self.dim**2,), dtype=np.float32), spaces.Discrete(2)))

        
    def check_done(self):
        is_done = False
        ganador = None

        #Ponemos el tablero en forma matricial para verlo más fácil
        tablero = copy(self.tablero) #Creo recordar que hacía falta esto para no romperlo todo
        tablero = np.reshape(tablero, (self.dim, self.dim))

        #Miramos si alguien ha ganado
        for i in range(self.dim): #Miramos horizontales y verticales
            if np.abs(np.sum(tablero[i])) == self.dim or np.abs(np.sum(tablero[:,i])) == self.dim:
                is_done = True
                if np.sum(tablero[i]) == self.dim:
                    ganador = 1
                else:
                    ganador = -1
            
        #Comprobamos diagonales
        if np.abs(np.trace(tablero)) == self.dim or np.abs(np.trace(np.fliplr(tablero))) == self.dim: #Al darle la vuelta podemos calcular las dos diagonales como la traza
            is_done = True
            ganador = 1

        elif 0 not in self.tablero:
            ganador = 0
            is_done = True

        return is_done, ganador

    def create_action(self, i):
        empty = np.array([0]*self.dim**2)
        if self.tablero[i] == 0:
            empty[i] = 1 #Si está vacía la posición i, le decimos que la puede coger marcándo con un 1
            return empty

    def available_positions(self):
        available_positions = []
        tablero = copy(self.tablero) #Per si de cas, que nunca se sabe

        for i in range(self.dim ** 2):
            position = self.create_action(i)
            available_positions.append(position)
        
        return available_positions

    def flip_ficha(self):
        if self.ficha == 1:
            return -1
        else:
            return 1
    
    def is_action_ok(self, action):
        is_ok = False

        for av_action in self.available_positions():
            if (action == av_action).all():
                is_ok = True
                break #No hace falta que compruebe el resto cuándo una le parezca bien
        
        return is_ok
    
    def step(self, action): #Aquí tiene que ir todo lo necesario para que haga un step y te devuelva el reward, el siguiente y si está donete
        #En principio la idea es que las acciones sean todo 0 menos 1/-1 en los lugares dónde puede colocar cosas, así podemos hacer esto así:
        

        if  not self.is_action_ok(action): #Si quiere poner una ficha dónde ya hay otra le quitas muntó de puntos y acabamos la partida
            reward = -10
            is_done = True #Terminamos la partida por tramposo
            next_obs = self.reset() #Pongo esto por poner algo, pero en realidad daría igual lo que le pongas
            extra = "¡No vale poner fichas dónde ya hay!"


        else: #Si la acción es válida pues ya entramos aquí
            reward = 0
            extra = "Jugando..."
            
            self.tablero += action * self.ficha #Ejecutamos la acción y multiplicamos con la ficha para ponerla
            self.ficha = self.flip_ficha() #Cambiamos la ficha

            next_obs = (self.tablero, self.ficha)
            is_done, ganador = self.check_done()

            if ganador is not None:
                if ganador == 0:
                    reward = 0.1
                    extra = "¡Empate!"
                else:
                    reward = 1
                    extra = "¡Has ganado!"
        
        return next_obs, reward, is_done, extra
        

    def reset(self): #Aquí hay que ponerle para que sepa volver al principio
        self.tablero = np.array([0]*self.dim**2)
        self.ficha = random.sample(self.fichas,1)[0] #Cogemos el número para que no nos devuelva una lista sino un número directamente

        return(self.tablero, self.ficha)

    def render(self, mode = "human"): #Y aquí para que sepa dibujarlo
        tablero_print = np.reshape(self.tablero, (self.dim, self.dim))
        print(tablero_print)

    def close(self): #Esto imagino que para chapar, pero no lo había visto nunca antes
        pass


# if __name__ == "__main__":
#     env = TicTacToe()
    
#     print("Estado inicial: {}".format(env.reset()))
#     print("Posiciones disponibles: {}".format(len(env.available_positions())))

#     #action = env.action_space.sample
#     test_action = env.action_space.sample()
#     print("Acción de prueba: {}".format(test_action))

#     next_obs, reward, is_done, game_state = env.step(test_action)
#     print("Next obs: {}\n Reward: {}\n Is_done: {}\n Game State: {}".format(next_obs, reward, is_done, game_state))

#     print("---------------------")

#     print("Vamos a darle un loopito random a ver klk:")
    
#     env.reset()
#     is_done = False

#     # while not is_done:
#     #     env.render()
#     #     test_action = env.action_space.sample()
#     #     print("Acción: {} -> {}".format(test_action, type(test_action)))
#     #     next_obs, reward, is_done, game_state = env.step(test_action)
    
#     # actions = [np.array([1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int), np.array([0, 1, 0, 0, 0, 0, 0, 0, 0], dtype=int), np.array([0, 0, 1, 0, 0, 0, 0, 0, 0], dtype=int),\
#     #      np.array([0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=int), np.array([0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=int), np.array([0, 0, 0, 0, 0, 1, 0, 0, 0], dtype=int),\
#     #          np.array([0, 0, 0, 0, 0, 0, 1, 0, 0], dtype=int), np.array([0, 0, 0, 0, 0, 0, 0, 1, 0], dtype=int), np.array([0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int)]
    
#     # for action in actions:
#     #     next_obs, reward, is_done, game_state = env.step(action)
#     #     if is_done:
#     #         break
    
#     env.render()
#     print("Next obs: {}\n Reward: {}\n Is_done: {}\n Game State: {}".format(next_obs, reward, is_done, game_state))