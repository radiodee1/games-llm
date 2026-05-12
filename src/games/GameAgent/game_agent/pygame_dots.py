#!/usr/bin/env python3

#PONG pygame

#import json
import random
import re
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
        self.l_score = 0
        self.r_score = 0
        self.paddle1_bounce = 0 
        self.paddle2_bounce = 0
        self.serves_num = 0

        
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

        self.total_samples = 9
        self.drawable_dots = []
        self.frame_info = []

        self.action_meaning = [ ]
        for i in range(self.total_samples):
            self.action_meaning += [ {'name': str(i), 'num': i , 'meaning': str(i) } ]

    def size_init(self):
        #print('smaller' , self.smaller)
        smaller = self.smaller

        self.WIDTH = 600 // smaller
        self.HEIGHT = 400 // smaller      
        self.BALL_RADIUS = 20 // smaller
        self.BORDER_SIZE = 24 // smaller
        self.fontsize = 48 // smaller
        #print('show_image', self.show_image)
        if self.show_image:
            pygame.display.set_caption('Dots')
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        else:
            self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.HIDDEN)
            pass

    def draw(self, canvas=None):
        if canvas == None:
            canvas = self.window
        canvas.fill(self.BLACK)
        i = math.floor(random.random() * self.total_samples - 1) + 1
        j = 0
        num = 0 
        while j <= i and num < 100:
            #for j in range(i):
            r = self.place_dot(j)
            if r != None:
                self.drawable_dots += [ { 'center' : r , 'radius' : self.BALL_RADIUS, 'color': self.WHITE } ]
                j += 1 
            else:
                num += 1 
        #print(len(self.drawable_dots), 'drawable_dots')
        self.frame_info += [ { 'computed': j, 'guess': None } ]
        self.draw_all_dots()
        self.message += ' computed=' + str(j  ) + ' ' 

    def place_dot(self, i):
        num = 0
        x = self.WIDTH // 2 
        y = self.HEIGHT // 2 
        center = (x, y)
        while num < 1000:
            x = math.floor( random.random() * (self.WIDTH - self.BALL_RADIUS) + self.BALL_RADIUS)
            y = math.floor( random.random() * (self.HEIGHT - self.BALL_RADIUS ) + self.BALL_RADIUS)
            center = (x, y)
            if  x + self.BALL_RADIUS < self.WIDTH and x - self.BALL_RADIUS > 0 and y + self.BALL_RADIUS < self.HEIGHT and y - self.BALL_RADIUS > 0:
                break 
            num += 1 

        num = 0 
        background_color = self.BLACK

        r = random.randint(0, 3)
        current_surface = pygame.display.get_surface()
        background_color = current_surface.get_at(center)
        while num < 1000:
            for i in range(x - self.BALL_RADIUS, x + self.BALL_RADIUS):
                for j in range(y - self.BALL_RADIUS, y + self.BALL_RADIUS):
                    if i <= 0 or i >= self.WIDTH or j <= 0 or j >= self.HEIGHT:
                        return None
                    if current_surface.get_at((i,j)) == self.WHITE:
                        background_color = self.WHITE
            if background_color == self.WHITE:
                if r == 0 and x - 2 > 0:
                    x = x - 2 
                elif r == 1 and x + 2 < self.WIDTH:
                    x = x + 2 
                elif r == 2 and y - 2 > 0:
                    y = y - 2
                elif r == 3 and y + 2 < self.HEIGHT:
                    y = y + 2
                else:
                    return None
                center = (x, y)
            else :
                pygame.draw.circle(self.window, self.WHITE, center, self.BALL_RADIUS, 0)
                return center
            num += 1 
        
        #print(i)
        return None

    def draw_all_dots(self):
        #print(self.drawable_dots)
        pass 

    def make_message(self) -> str:
        return "\n---\ncount the dots in the image.\n---\n"

    def image_save(self, filename):
        self.pygame_save(filename)

    def pygame_save(self, f):
        print(f)
        border_rect = pygame.Surface((self.WIDTH + 2 * self.BORDER_SIZE, self.HEIGHT + 2 * self.BORDER_SIZE))
        border_rect.fill(self.GRAY)
        border_rect.blit(self.window, (self.BORDER_SIZE, self.BORDER_SIZE))

        pygame.image.save(border_rect, f)

    def stats(self, short=True):
        y = 0
        if short:
            x = int(self.action_string)
            if self.frame_info[-1]['guess'] == None:
                self.frame_info[-1]['guess'] = x 
        else:
            x = 0 
            for i in self.frame_info:
                if i['guess'] == i['computed']:
                    x += 1 
            y = x / len(self.frame_info)
            y = math.floor(y * 100)
        super().stats(short)
        if not short:
            print('percent right' , y)
