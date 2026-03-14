#!/usr/bin/env python3

import gymnasium as gym 
import sys 
import pygame
import cv2

class DefaultBare:

    def __init__(self, mode="rgb_array") -> None:
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None

        self.smaller = 4 
        smaller = self.smaller
        self.auto = True
        self.text_input = True
        self.small_test = -1 ## set to -1 for 'no test'
        self.vel_const = 8 // smaller
        self.vel_const_right = 4 // smaller # 16!
        self.skip = 4
        self.num = 0 
        self.message = ''
        self.fontsize = 48 // smaller
        #self.LOCAL_LLM = ''

        self.prompt_list = []

        self.acceleration = .25
        self.sudden_death_score = -1
        self.disable_thinking = True
        self.context_size = 4096
        self.use_chat = True
        self.queue_len = 4 
        self.commands = []
        self.random_threshold = 50
        self.no_llm = -1 
        self.image_strip = -1 
        self.strip = []
        self.stream_requests = False
        self.stream_openai = False 
        self.scrape_general = False
        self.video_openai = False
        self.double_arrow = False
        self.use_hinting = False
        self.image_series = False
        self.prompt_strategy = 1 
        self.make_corpus = -1
        self.corpus_offset = 0
        self.paddle_message = ''
        self.temperature = -1 
        self.top_p = -1 

        self.show_image = True 

        pass 

    def pygame_save(self, f):
        print(f)
        pass 

    def image_save(self, filename):
        self.pygame_save(filename)
        pass

    def make_message(self) -> str:
        return ""

    def draw(self, surface=None):
        pass 

    def init(self):
        pass 

    def reset(self):
        pass 

class DefaultPlugin (DefaultBare):

    def __init__(self, mode="rgb_array") -> None:
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
        cv2.destroyAllWindows()
        pass 
    
    def image_save(self, filename):
        pass 

    def pygame_save(self, f):
        if self.render_mode != 'rgb_array':
            return
        r = self.env.render()
        surface = pygame.surfarray.make_surface(r)
        surface = pygame.transform.rotate(surface, 270)
        surface = pygame.transform.flip(surface, True, False)
        pygame.image.save(surface, f)

        if self.show_image:
            frame_bgr = cv2.cvtColor(r, cv2.COLOR_RGB2BGR)
            cv2.imshow('', frame_bgr)
            cv2.waitKey(1)

        pass 

