#!/usr/bin/env python3

import gymnasium as gym
import ale_py
import sys 
import pygame
import cv2
import base64

class DefaultBare:

    def __init__(self, mode="rgb_array") -> None:
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None
        self.truncated = False
        self.terminated = False

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
        self.window = None

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
        self.action_meaning = [] # combined meaning information
        self.meaning = [] # just the human readable meaning

        self.fps = None
        self.show_image = True 

        self.l_score = 0
        self.r_score = 0
        pass 

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    def pygame_save(self, f):
        pass

    def image_save(self, filename):
        self.pygame_save(filename)
        pass

    def make_message(self) -> str:
        self.read_actions()
        print(self.action_meaning, 'meaning')
        m = [ str( '"' + i['meaning'] + '"') for i in self.action_meaning ]
        print(m, 'm')
        txt = self.message + ' ' 
        txt += 'These are the actions you can take: ' + ', '.join(m)
        return str(txt)

    def read_actions(self):
        if isinstance(self.env.action_space, gym.spaces.Discrete):
            
            x = self.env.unwrapped.get_action_meanings()
            print(x, 'x')
            self.action_meaning = []
            num = 0
            for i in range(len(x)):
                if self.meaning == None or len(self.meaning) == 0:
                    m = x[i]
                else:
                    m = self.meaning[i]
                if m != None: 
                    self.action_meaning += [ { 'name' : x[i], 'num': num, 'meaning': m  } ]
                num += 1 
            print(self.action_meaning)

    def no_description(self):
        pass 

    def stats(self, short=True):
        if short:
            return
        print(self.commands)
        return 

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
        self.r_score += reward
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
        self.pygame_save(filename)
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
            #print(f, 'cv2')
            frame_bgr = cv2.cvtColor(r, cv2.COLOR_RGB2BGR)
            cv2.imshow('', frame_bgr)
            cv2.waitKey(1)

        pass 
    
    def no_description(self):
        ## no description available??
        self.action_meaning = []
        num = 0 
        x = range(self.env.action_space.n) #[ '0', '1', '2', '3'  ]
        for i in range(len(x)):
            if i <= len(self.meaning) and self.meaning[i] != None:
                self.action_meaning += [ { 'name' : x[i], 'num': num, 'meaning': self.meaning[i]} ]
            num += 1 


