#!/usr/bin/env python3

#PONG pygame

#import json
import random
import pygame #, sys
from pygame.locals import *
#import os 
import time
#import subprocess
import base64
#import argparse 
import math
from . import DefaultBare
#from query import  Oai, Ollama, Gem, Mis 

class PygameDotAgent(DefaultBare):

    def __init__(self, mode='human', inverse_size=4, show_image=True) -> None:
        super().__init__(mode=mode, inverse_size=inverse_size, show_image=show_image)
        self.size_init() 
        pygame.init()
        self.fps = pygame.time.Clock()
        self.start_time = time.perf_counter()

        self.model = ''
        #size adjustment
        self.smaller = inverse_size

        #colors
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLACK = (10,10,10)
        self.GRAY = (100,100,100)
        self.BLUE = (0,0,255)

        #globals
        smaller = self.smaller
        self.WIDTH = 600 // smaller
        self.HEIGHT = 400 // smaller      
        self.BALL_RADIUS = 20 // smaller
        self.PAD_WIDTH = 16 // smaller
        self.PAD_HEIGHT = 80 // smaller
        self.HALF_PAD_WIDTH = self.PAD_WIDTH // 2
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT // 2
        self.ball_pos = [0,0]
        self.ball_vel = [0,0]
        self.paddle1_pos = [0,0]
        self.paddle2_pos = [0,0]
        self.paddle1_vel = 0
        self.paddle2_vel = 0
        self.l_score = 0
        self.r_score = 0
        self.trace_pos = [0,0] 
        self.paddle1_bounce = 0 
        self.paddle2_bounce = 0
        self.serves_num = 0

        self.action_meaning = [ ]
        
        self.BORDER_SIZE = 24 // smaller

        self.auto = True
        self.text_input = True
        self.small_test = -1 ## set to -1 for 'no test'
        self.vel_const = 8 // smaller
        self.vel_const_right = 4 // smaller # 16!
        self.skip = 1
        self.num = 0 
        self.message = ''
        self.fontsize = 48 // smaller
        self.LOCAL_LLM = 'http://localhost:11434/api/'

        self.prompt_list = [ '1', '2', '3']

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
        self.video = False
        self.double_arrow = False
        self.use_hinting = False
        self.image_series = False
        self.prompt_strategy = 1 
        self.make_corpus = -1
        self.corpus_offset = 0
        self.paddle_message = ''
        self.temperature = -1 
        self.top_p = -1 

        self.arrow_surface = None ## for arrow...


    def size_init(self):
        #print('smaller' , self.smaller)
        smaller = self.smaller

        self.WIDTH = 600 // smaller
        self.HEIGHT = 400 // smaller      
        self.BALL_RADIUS = 20 // smaller
        self.PAD_WIDTH = 16 // smaller
        self.PAD_HEIGHT = 80 // smaller
        self.HALF_PAD_WIDTH = self.PAD_WIDTH // 2
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT // 2
        self.BORDER_SIZE = 24 // smaller
        self.vel_const = 8 // smaller
        self.vel_const_right = 4 // smaller # 16!
        self.fontsize = 48 // smaller
        print('show_image', self.show_image)
        if self.show_image:
            pygame.display.set_caption('Pong')
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        else:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HIDDEN)
            pass



