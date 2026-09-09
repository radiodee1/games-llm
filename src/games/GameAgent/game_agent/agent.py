

from .default import DefaultPlugin


class LunarLanderAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
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

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.agent = 'PongNoFrameskip-v4'
        #self.agent = 'Pong-v4'
        self.action = 0
        self.prompt_string = (
                "Pong! Return the ball to the oponent and score to win the game."
                " You are the right paddle. Your paddle is green. Ignore the SCORE at the top of the screen."
                # " Calculate the change in x and the change in y to predict where the ball is going."
                " Notice the y position of the ball."
                " If the ball is higher than you, move up. If the ball is lower than you, move down."
                " If the paddle is lined up to hit the ball, wait."
                " Show some of your thinking process and then give your final answer."
        )
        #self.prompt_string = "Describe the contents of this picture."
        self.meaning = [ 'control.move.wait', 'control.move.serve', 'control.move.up', 'control.move.down', None, None ]

    def start_sequence(self):
        self.action = 0
        if self.frame_skip == None:
            frame_skip = 1
        else:
            frame_skip = self.frame_skip
        for i in range(58 // frame_skip ):
            self.draw()
        return super().start_sequence()

    def draw(self, surface=None):
        x = super().draw(surface)
        if self.reward > 0:
            self.r_score += int(abs(self.reward))
        if self.reward < 0:
            self.l_score += int(abs(self.reward))
        return x 

class BreakoutAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.agent = 'BreakoutNoFrameskip-v4'
        #self.agent = ''
        self.action = 0
        self.prompt_string = (
                "Breakout! Return the ball and break down the wall to win the game."
                " You are on the bottom of the screen. Hit the ball to break up the wall and gain points."
                " You can move your paddle to the right or left. You can only do one action at a time."
                " Show some of your thinking process and then give your final answer."
        )
        self.meaning = [ 'control.move.wait', 'control.move.serve', 'control.move.right', 'control.move.left' ]


    def draw(self, surface=None):
        x = super().draw(surface)
        if self.reward > 0:
            self.r_score += int(abs(self.reward))
        if self.reward < 0:
            self.l_score += int(abs(self.reward))
        return x 

class PongVjepa2Agent (PongAgent):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.meaning = [ 'wait', 'serve', 'right.move.up', 'right.move.down' , 'left.move.up', 'left.move.down']
        self.agent ='PongNoFrameskip-v4' 
        self.prompt_string = ''

    def scrape(self, txt, replace=False):
        self.action_string = ''
        self.action = None
        return super().scrape(txt, replace)
