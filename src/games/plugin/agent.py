

from .default import DefaultPlugin


class LunarLanderAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'LunarLander-v3'
        self.prompt_string = "LunarLander! Land the spacecraft on the spot between the flags."
        self.meaning = ['NOOP', 'GO_LEFT', 'MAIN_ENGINE', 'GO_RIGHT']

    def read_actions(self):
        ## no description available??
        self.no_description()
        print(self.action_meaning)

    def start_sequence(self):
        self.action = 0 
        for i in range(5 // self.frame_skip ):
            self.draw()
        return super().start_sequence()

class PongAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'ALE/Pong-v5'
        #self.agent = 'PongNoFrameskip-v4'
        #self.frame_skip = 4 
        self.prompt_string = "Pong! Return the ball to the oponent and score to win the game."
        self.meaning = [ 'control.move.wait', 'control.move.serve', 'control.move.up', 'control.move.down', None, None ]
        #self.meaning = [ 'control.move.serve', None, 'control.move.up', 'control.move.down', None, None ]

    def start_sequence(self):
        self.action = 0 
        for i in range(52 // self.frame_skip ):
            self.draw()
        return super().start_sequence()
