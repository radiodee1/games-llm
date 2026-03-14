

from .default import DefaultPlugin


class LunarLanderAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'LunarLander-v3'
        self.message = "Land the spacecraft on the spot between the flags."

    def read_actions(self):
        ## no description available??
        self.action_meaning = []
        num = 0 
        x = [ '0', '1', '2', '3'  ]
        for i in x:
            self.action_meaning += [ { 'name' :'control.' + i, 'num': num, 'meaning': ""} ]
            num += 1 
        print(self.action_meaning) 

class PongAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'ALE/Pong-v5'
        self.message = "Pong! Return the ball to the oponent and score to win the game."
