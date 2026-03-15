

from .default import DefaultPlugin


class LunarLanderAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'LunarLander-v3'
        self.message = "LunarLander! Land the spacecraft on the spot between the flags."
        self.meaning = ['NOOP', 'LEFT_ENGINE', 'MAIN_ENGINE', 'RIGHT_ENGINE']

    def read_actions(self):
        ## no description available??
        self.no_description()

class PongAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'ALE/Pong-v5'
        self.message = "Pong! Return the ball to the oponent and score to win the game."
