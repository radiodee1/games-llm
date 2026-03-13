#!/usr/bin/env python3

import gymnasium as gym 
import sys 

class DefaultBare:

    def __init__(self, mode="human") -> None:
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None
        pass 

    def draw(self, surface=None):
        pass 

    def init(self):
        pass 

    def reset(self):
        pass 

class DefaultPlugin (DefaultBare):

    def __init__(self, mode="human") -> None:
        super().__init__(mode)
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None
        self.truncated = False
        self.terminated = False
        pass 

    def draw(self, surface=None):
        if surface != None:
            sys.exit()
        observation, reward, terminated, truncated, info = self.env.step(self.action)
        self.terminated = terminated
        self.truncated = truncated
        pass 

    def init(self):
        self.env = gym.make(self.agent, render_mode=self.render_mode)
        pass 

    def reset(self):
        self.truncated = False
        self.terminated = False
        observation, info = self.env.reset()
        pass 


