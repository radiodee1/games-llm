#!/usr/bin/env python3

#PONG pygame

#import json
import random
import pygame, sys
from pygame.locals import *
import os 
import time
#import subprocess
import base64
import argparse 
import math
from plugin import DefaultBare
#from query import  Oai, Ollama, Gem, Mis 

from dotenv import load_dotenv 

load_dotenv()


model = "qwen3-vl:2b"
model_class = None 

whitelist = {
    'qwen3-vl:2b'   : 'Ollama',
    'qwen3-vl:4b'   : 'Ollama',
    'gpt-5.2'       : 'Oai',
    'gpt-4o'        : 'Oai',
    'gemini-3-flash-preview' : 'Gem',
    'gemini-3-pro-preview'   : 'Gem',
    'gemini-3.1-pro-preview' : 'Gem',
    'gemini-2.5-flash'       : 'Gem',
    #'gemini-3-pro-image-preview' : 'Gem',
    'mistral-large-2512'     : 'Mis',
    'pixtral-large-2411'     : 'Mis'
}

plugin_class = None

class PygamePongAgent(DefaultBare):

    def __init__(self, mode='human') -> None:
        super().__init__(mode)
        pass
        pygame.init()
        self.fps = pygame.time.Clock()
        self.start_time = time.perf_counter()

        self.model = ''
        #size adjustment
        self.smaller = 4
        self.window = None

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

        self.BORDER_SIZE = 24 // smaller

        self.auto = True
        self.text_input = True
        self.small_test = -1 ## set to -1 for 'no test'
        self.vel_const = 8 // smaller
        self.vel_const_right = 4 // smaller # 16!
        self.skip = 4
        self.num = 0 
        self.message = ''
        self.fontsize = 48 // smaller
        self.LOCAL_LLM = 'http://localhost:11434/api/'

        self.prompt_list = ['Describe the arrow in this picture. What direction is it pointing? What is its up/down angle?' , 
                       'My name is David.', 
                       'What is my name?', 
                       'What is your favorate color?' ]

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

        self.arrow_surface = None ## for arrow...
        pygame.display.set_caption('Pong')

    def size_init(self):

        #global WIDTH, HEIGHT, BALL_RADIUS, PAD_WIDTH, PAD_HEIGHT, HALF_PAD_WIDTH, HALF_PAD_HEIGHT, BORDER_SIZE
        #global vel_const, vel_const_right, fontsize, smaller 
        
        print('smaller' , self.smaller)
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


    # helper function that spawns a ball, returns a position vector and a velocity vector
    # if right is True, spawn to the right, else spawn to the left
    def ball_init(self, right):
        #global ball_pos, ball_vel # these are vectors stored as lists
        #global serves_num, message

        self.ball_pos = [self.WIDTH//2,self.HEIGHT//2]
        self.horz = random.randrange(2,4)
        self.vert = random.randrange(1,3)
        
        if right == False:
            self.horz = - self.horz
            
        self.ball_vel = [self.horz, - self.vert]
        self.serves_num += 1 
        self.message += "Serve!!"

    # define event handlers
    def init(self):
        #global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
        #global score1, score2, arrow_surface  

        self.paddle1_pos = [self.HALF_PAD_WIDTH - 1, self.HEIGHT//2]
        self.paddle2_pos = [self.WIDTH +1 - self.HALF_PAD_WIDTH, self.HEIGHT//2]
        self.l_score = 0
        self.r_score = 0
        if random.randrange(0,2) == 0:
            self.ball_init(True)
        else:
            self.ball_init(False)
        self.arrow_surface = self.draw_arrow() 

    #draw function of canvas
    def draw(self, canvas):
        #global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
        #global message, num, skip, trace_pos, paddle1_bounce, paddle2_bounce, random_threshold 
        #global make_corpus, paddle_message

        canvas.fill(self.BLACK)
        pygame.draw.line(canvas, self.WHITE, [self.WIDTH // 2, 0],[self.WIDTH // 2, self.HEIGHT], 1)
        pygame.draw.line(canvas, self.WHITE, [self.PAD_WIDTH, 0],[self.PAD_WIDTH, self.HEIGHT], 1)
        pygame.draw.line(canvas, self.WHITE, [self.WIDTH - self.PAD_WIDTH, 0],[self.WIDTH - self.PAD_WIDTH, self.HEIGHT], 1)
        pygame.draw.circle(canvas, self.WHITE, [self.WIDTH//2, self.HEIGHT//2], 70 // self.smaller, 1)

        # update paddle's vertical position, keep paddle on the screen
        if self.make_corpus < 0:
            computer = random.random() 
            if not self.auto:
                if self.paddle1_pos[1] > self.HALF_PAD_HEIGHT and self.paddle1_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
                    self.paddle1_pos[1] += self.paddle1_vel 
                elif self.paddle1_pos[1] == self.HALF_PAD_HEIGHT and self.paddle1_vel > 0:
                    self.paddle1_pos[1] += self.paddle1_vel
                elif self.paddle1_pos[1] == self.HEIGHT - self.HALF_PAD_HEIGHT and self.paddle1_vel < 0:
                    self.paddle1_pos[1] += self.paddle1_vel 
            if self.auto and self.num % self.skip == 0 and computer <= self.random_threshold / 100:
                if self.paddle1_pos[1] >= int(self.ball_pos[1]) and self.ball_vel[1] < 0:  
                    self.paddle1_pos[1] -= abs(self.vel_const) * self.skip # up - negative 
                    print('computer paddle up', - abs(self.vel_const) * self.skip)
                elif self.paddle1_pos[1] <= int(self.ball_pos[1]) and self.ball_vel[1] > 0:  
                    self.paddle1_pos[1] += abs(self.vel_const) * self.skip # down - positive
                    print('computer paddle down', abs(self.vel_const) * self.skip)
            elif self.auto and self.num % self.skip == 0:
                print('pass because of threshold', computer * 100)

            if self.paddle2_pos[1] > self.HALF_PAD_HEIGHT and self.paddle2_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
                self.paddle2_pos[1] += int(self.paddle2_vel)
            if self.paddle2_pos[1] < self.HALF_PAD_HEIGHT + int(self.paddle2_vel) and int(self.paddle2_vel) > 0:
                self.paddle2_pos[1] += int(self.paddle2_vel)
            if self.paddle2_pos[1] > self.HEIGHT - self.HALF_PAD_HEIGHT - int(self.paddle2_vel) and int(self.paddle2_vel) < 0:
                self.paddle2_pos[1] += int(self.paddle2_vel)

            if self.paddle2_pos[1] <= self.HALF_PAD_HEIGHT  and int(self.paddle2_vel) > 0:
                self.paddle2_pos[1] += int(self.paddle2_vel)
            if self.paddle2_pos[1] >= self.HEIGHT - self.HALF_PAD_HEIGHT and int(self.paddle2_vel) < 0:
                self.paddle2_pos[1] += int(self.paddle2_vel)

        elif self.make_corpus > 0 and self.num % self.skip == 0 :
            paddle2_message = ''
            temp1_vel, paddle1_message = self.paddle_auto_vel(self.paddle1_pos, self.ball_pos, self.ball_vel, self.vel_const)
            self.paddle1_pos[1] += temp1_vel * self.skip 
            temp2_vel, paddle2_message = self.paddle_auto_vel(self.paddle2_pos, self.ball_pos, self.ball_vel, self.vel_const_right)
            self.paddle2_pos[1] += temp2_vel * self.skip
            #print( paddle1_pos, paddle1_message, paddle2_pos, 'paddles', paddle2_message, vel_const, vel_const_right )
            self.paddle_message = paddle2_message

        if self.num % self.skip == 0:
            self.trace_pos[0] = self.ball_pos[0] - self.ball_vel[0] * ( 4 // self.smaller )  
            self.trace_pos[1] = self.ball_pos[1] - self.ball_vel[1] * ( 4 // self.smaller )

        #update ball
        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        #draw paddles and ball
        if not self.double_arrow:
            pygame.draw.circle(canvas, self.GRAY, self.trace_pos, self.BALL_RADIUS, 0)
        self.blit_rotate_arrow(canvas, self.arrow_surface, self.ball_pos, self.ball_vel)
        pygame.draw.circle(canvas, self.RED, self.ball_pos, self.BALL_RADIUS, 0)
        paddle1_points = [[self.paddle1_pos[0] - self.HALF_PAD_WIDTH, self.paddle1_pos[1] - self.HALF_PAD_HEIGHT], [self.paddle1_pos[0] - self.HALF_PAD_WIDTH, self.paddle1_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle1_pos[0] + self.HALF_PAD_WIDTH, self.paddle1_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle1_pos[0] + self.HALF_PAD_WIDTH, self.paddle1_pos[1] - self.HALF_PAD_HEIGHT]]
        paddle2_points = [[self.paddle2_pos[0] - self.HALF_PAD_WIDTH, self.paddle2_pos[1] - self.HALF_PAD_HEIGHT], [self.paddle2_pos[0] - self.HALF_PAD_WIDTH, self.paddle2_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle2_pos[0] + self.HALF_PAD_WIDTH, self.paddle2_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle2_pos[0] + self.HALF_PAD_WIDTH, self.paddle2_pos[1] - self.HALF_PAD_HEIGHT]]
        
        pygame.draw.polygon(canvas, self.GREEN, paddle1_points, 0)
        pygame.draw.polygon(canvas, self.GREEN, paddle2_points, 0)
        
        self.stripe_polygon(canvas, paddle1_points, self.WHITE, 8 // self.smaller, 16 // self.smaller)
        self.stripe_polygon(canvas, paddle2_points, self.BLUE, 8 // self.smaller, 16 // self.smaller)

        #ball collision check on top and bottom walls
        if int(self.ball_pos[1]) <= self.BALL_RADIUS:
            self.ball_vel[1] = - self.ball_vel[1]
            self.message = "Bounce!!"
        if int(self.ball_pos[1]) >= self.HEIGHT + 1 - self.BALL_RADIUS:
            self.ball_vel[1] = -self.ball_vel[1]
            self.message = "Bounce!!"
        
        #ball collison check on gutters or paddles
        if int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH and int(self.ball_pos[1]) in range(int(self.paddle1_pos[1]) - self.HALF_PAD_HEIGHT, int(self.paddle1_pos[1]) + self.HALF_PAD_HEIGHT,1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= (1.0 + self.acceleration)
            self.ball_vel[1] *= (1.0 + self.acceleration)
            self.paddle1_bounce += 1 
            self.message = "Uh oh!!"
        elif int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH:
            self.r_score += 1
            self.message = "Score!!"
            self.ball_init(True)
            
        if int(self.ball_pos[0]) > self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH and int(self.ball_pos[1]  ) > int(self.paddle2_pos[1]) - self.HALF_PAD_HEIGHT - abs(int( self.BALL_RADIUS)) and int(self.ball_pos[1]  ) < int(self.paddle2_pos[1]) + self.HALF_PAD_HEIGHT + abs(int(self.BALL_RADIUS)):  
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= (1.0 + self.acceleration)
            self.ball_vel[1] *= (1.0 + self.acceleration)
            self.paddle2_bounce += 1 
            self.message = "Nice!!"
        elif int(self.ball_pos[0]) > self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH:
            self.l_score += 1
            self.message = "Ouch!!"
            self.ball_init(False)
        
        if self.use_hinting:
            hint_x = self.WIDTH - self.PAD_WIDTH 
            hint_y = self.get_hint_y() 
            if self.is_hint_now(hint_y):
                pygame.draw.line(canvas, self.RED, (hint_x, hint_y), (hint_x + 2, hint_y), 8)

        #update scores
        myfont1 = pygame.font.SysFont("Comic Sans MS", self.fontsize)
        label1 = myfont1.render("Score "+str(self.l_score), 1, (255,255,0))
        canvas.blit(label1, (50 // self.smaller, 20 // self.smaller))

        myfont2 = pygame.font.SysFont("Comic Sans MS", self.fontsize)
        label2 = myfont2.render("Score "+str(self.r_score), 1, (255,255,0))
        canvas.blit(label2, (410 // self.smaller, 20 // self.smaller)) 

        pygame.display.update([canvas.get_rect()])

    def stripe_polygon(self, canvas, polygon, color, width, seperation):
        ul, ur, lr, ll = polygon
        slant = 0 # 4 
        x1, y1 = ul
        x2, y2 = lr 
        for i in range(y1, y2, seperation + width):
            pygame.draw.line(canvas, color, (x1, i), (x2, i + slant), width )
        pass 

    def draw_arrow(self):
        #global double_arrow, smaller
        # -->
        xoffset = 100 # // smaller # 25 ## 35! 
        arrow_lines = [
            (self.BLUE, (160, 0),   (200, 20), 8 // self.smaller  ),  # angle line
            (self.BLUE, (120, 20),  (200, 20), 8 // self.smaller  ),  # horizontal line
            (self.BLUE, (160, 48),  (200, 20), 8 // self.smaller  ),  # angle line
        ]
        arrow_surface = pygame.Surface((400 // self.smaller, 48 // self.smaller), pygame.SRCALPHA)
        xoffset = 100 # // smaller # 25 
        smaller = self.smaller
        for color, start_pos, end_pos, width in arrow_lines:
            start_pos = (start_pos[0]  + xoffset) // smaller , start_pos[1] // smaller
            end_pos = (end_pos[0]  + xoffset) // smaller, end_pos[1] // smaller
            pygame.draw.line(arrow_surface, color, start_pos, end_pos, width)
        
        if self.double_arrow:
            xoffset = - 80 #// smaller #20 
            for color, start_pos, end_pos, width in arrow_lines:
                start_pos = (start_pos[0]  + xoffset) // smaller, start_pos[1] // smaller
                end_pos = (end_pos[0]  + xoffset) // smaller, end_pos[1] // smaller
                pygame.draw.line(arrow_surface, color, start_pos, end_pos, width)
        return arrow_surface

    def blit_rotate_arrow(self, surf, image, center,  ball_vel):
        angle_part = 0 
        xvel =  ball_vel[0]
        yvel = - ball_vel[1]
        if xvel == 0:
            xvel = 0.1 
        if xvel > 0 and yvel > 0:
            angle_part = 0 
        if xvel < 0 and yvel > 0:
            angle_part = 180 
        if xvel < 0 and yvel < 0:
            angle_part = 180  
        if xvel > 0 and yvel < 0:
            angle_part = 0 

        angle_radians = math.atan(  yvel / xvel )
        angle = math.degrees(angle_radians) + angle_part
        rotated_image =  pygame.transform.rotate(image, angle)
        c = image.get_rect(center=center).center 
        new_rect = rotated_image.get_rect(center=c)
        surf.blit(rotated_image, new_rect)

    def get_hint_y(self):
        #global ball_pos, self.ball_vel 
        vx, vy = self.ball_vel
        if vx == 0:
            vx = 0.01
        m = vy / vx 
        b = self.ball_pos[1] - m * self.ball_pos[0] 
        hint_y = m * ( self.WIDTH - self.PAD_WIDTH ) + b 
        print('hint_y', hint_y)
        return int(hint_y)

    def is_hint_now(self, hint_y):
        #global ball_pos, ball_vel, self.paddle2_pos  
        is_facing_right = False
        if self.ball_vel[0] > 0:
            is_facing_right = True
        if self.paddle2_pos[1] - self.HALF_PAD_HEIGHT < hint_y and self.paddle2_pos[1] + self.HALF_PAD_HEIGHT > hint_y and is_facing_right:
            return True
        else:
            return False

    def paddle_auto_vel(self, paddle_pos, ball_pos, ball_vel, vel_const=2):
        if paddle_pos[0] < self.WIDTH // 2:
            #left 
            if paddle_pos[1] >= int(self.ball_pos[1]) and ball_vel[1] < 0:  
                return (- abs(vel_const) , 'control.move.up' )  # up - negative 
            elif paddle_pos[1] <= int(self.ball_pos[1]) and ball_vel[1] > 0:  
                return (+ abs(vel_const) , 'control.move.down') # down - positive
            return (0, 'control.move.wait')
        else:
            #right 
            i = self.get_hint_y()
            if i < 0 or i > self.HEIGHT:
                return (0 , 'control.move.wait')
            if i > paddle_pos[1] - self.HALF_PAD_HEIGHT and i < paddle_pos[1] + self.HALF_PAD_HEIGHT:
                return (0 , 'control.move.wait')
            if paddle_pos[1] >= i: 
                return (- abs(vel_const), 'control.move.up')
            elif paddle_pos[1] <= i: 
                return (+ abs(vel_const), 'control.move.down')
            return(0, 'control.move.wait')
        pass 

    def label(self, i, ii):
        myfont = pygame.font.SysFont(None, 16 )
        label1 = myfont.render("# " + str(ii), True, (255,255,0), self.GRAY)
        label1_rect = label1.get_rect();
        label1_rect.center = (self.WIDTH // 2 + self.BORDER_SIZE , int(self.HEIGHT + self.BORDER_SIZE - 2) )
        i.blit(label1, label1_rect )
        return i 

    def make_message(self):
        #global l_score, r_score, message, commands, prompt_strategy
        if self.use_hinting:
            hint_y = self.get_hint_y()

        title = 'Turn-based Pong or Tennis game. AI vs computer.'
        old_controls = (
                    ' Estimate the angle of the ball from the arrow and move your paddle to the position where you can hit the ball back to the other side.\n'
                    ' Enter "control.move.up" or "control.move.down" to move the Paddle in anticipation of the ball.'  
                    ' The paddle only moves up and down.'
                    ' Enter "control.move.wait" to skip one turn.'        
                    ' The ball is red. The ball is moving in the direction of the arrow. The arrows are blue.'                
                    ' You, the AI, are the right paddle.' 
                    ' Your paddle is blue and green. It is very small.' 
                    ' You move your paddle a small amount from where it already is.\n')

        new_controls = ('\n You, the AI, are the blue and green paddle. Solve this problem in steps: \n'
                    '1. Notice the position of the ball. What is its HEIGHT or Y value? \n'
                    '2. Notice the position of the right paddle. It is blue and green. What is the HEIGHT? \n'
                    '3. Calculate the horizontal line that comes from the ball across the screen.\n' 
                    '4. Keep the paddle always at the height of the ball. \n'
                    '5. Enter "control.move.up" or "control.move.down" to move the Paddle to the ball.\n'
                    ' You move your paddle a small amount from where it already is.\n'
                    ' Hit the ball in the MIDDLE of the paddle. If the ball passes the paddle you will lose a point.\n')
        
        third_controls = (
                    '\n1. Notice the position of the ball. What is its VERTICAL or Y value? What is its HORIZONTAL or X value?\n'
                    '2. Notice the angle of the ARROWS. What is their degree?\n'
                    '3. Is the ball moving to the right side?\n'
                    '4. Calculate the diagonal line that starts with the ball and follows the arrow all the way to the right side of the screen.\n'
                    '5. Note the place where the diagonal line crosses the goal line. This is where the ball will go.\n'
                    '6. Adjust the paddle to the anticipated position of the ball.\n'
                    '7. Enter "control.move.up" or "control.move.down" to move the Paddle.\n' 
                    '8. If the paddle is already in the right position, enter "control.move.wait" to skip one turn.\n'
                    )

        control_list = [ old_controls, new_controls, third_controls ]

        controls = control_list[ self.prompt_strategy - 1 ]

        controls += ('NOTE:\n'
                    ' Your paddle is blue and green. It is very small.\n'
                    ' The paddle only moves up and down.\n'
                    ' Enter "control.move.wait" to skip one turn.\n'        
                    ' The ball is red. The ball is moving in the direction of the arrows. The arrows are blue.\n'  
                    ' The left paddle moves on its own.\n'
                     #' Hit the ball when it comes to you.\n'
                     #' This is the only way to win.\n'
                    ' Your paddle does not need to be moving to hit the ball.\n'
                     )

        score = 'Their score ' + str(self.l_score) + ' / Your score ' + str(self.r_score) + ' - Left Bounces ' + str(self.paddle1_bounce) + ' / Right Bounces ' + str(self.paddle2_bounce)
        
        # limit = 'Answer in one line under 20 characters.'
        
        limit = 'Show your thinking and then reply with your final answer.'
        hint = ' Hint: Wait right there!'
        r = ''
        if self.use_hinting and self.is_hint_now(hint_y):
            controls += hint 
        if self.disable_thinking:
            limit = limit + ' Do not use thinking.'
        if len(self.message) > 0:
            r = self.message + ' - '
            #commands.append(str('--' + message + '--')) ## keep array size the same as step_count

        r = r + title + ' - ' + score + ' - ' + controls +  ' AI must use the picture and reply to play the game!' + ' ' + limit
        return r 

    def stats(self, short=True):
        #global paddle1_bounce, paddle2_bounce, l_score, r_score, num, skip, commands, step_count, serves_num 
        #global model
        print("model:", self.model)
        print("serves_num:", self.serves_num)
        print("Left-bounces:", self.paddle1_bounce, 'Right-bounces:', self.paddle2_bounce)
        print("l_score:", self.l_score, "r_score:", self.r_score)
        single = 0 
        if not short:
            single = 1 
        print("step-count:", (self.step_count + single))
        
        self.end_time = time.perf_counter()
        elapsed_min = (self.end_time - self.start_time) // 60 
        elapsed_sec = (self.end_time - self.start_time) - elapsed_min * 60
        elapsed_sec = '0000' + str(int(elapsed_sec))
        elapsed_sec = elapsed_sec[-2:]
        print(f"Elapsed time: {elapsed_min:.0f}:{elapsed_sec} minutes")
        print('---')
        if short:
            return
        num = 0 
        for i in self.commands:
            print(num + 1, i)
            num += 1 

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    def pygame_save(self, f):
        #global image_strip, strip, window 
        #global WIDTH, HEIGHT, BORDER_SIZE, GRAY

        print(f)
        border_rect = pygame.Surface((self.WIDTH + 2 * self.BORDER_SIZE, self.HEIGHT + 2 * self.BORDER_SIZE))
        border_rect.fill(self.GRAY)
        border_rect.blit(self.window, (self.BORDER_SIZE, self.BORDER_SIZE))

        #pygame.display.update([border_rect.get_rect()])

        if  self.image_strip < 0:
            pygame.image.save(border_rect, f)
        elif self.image_strip > 0 :
            self.strip.append(border_rect.copy() )
            i = 0 
            while len(self.strip) > self.image_strip and i < 10:
                self.strip.pop(0)
                print('pop strip img', len(self.strip))
                i += 1
            window_strip = pygame.Surface(( (self.WIDTH + 2 * self.BORDER_SIZE) * len(self.strip) , self.HEIGHT + 2 * self.BORDER_SIZE))
            window_strip.fill(self.GRAY)
            #pygame.display.update([window_strip.get_rect()])
            ii = 0 
            for i in self.strip:
                #pygame.display.update([i.get_rect()])
                if self.image_strip > 1:
                    i = self.label(i, ii + 0) 
                #pygame.display.update([i.get_rect()])
                window_strip.blit(i, ((self.WIDTH + 2 * self.BORDER_SIZE) * ii, 0))
                #pygame.display.update([window_strip.get_rect()])
                ii += 1 
            
            pygame.image.save(window_strip, f)
            #pygame.display.update([window_strip.get_rect()])


def parse():
    #global use_chat, auto, text_input, small_test, sudden_death_score, model, skip, smaller 
    #global LOCAL_LLM, queue_len, context_size, disable_thinking, random_threshold, image_strip, no_llm
    #global stream_requests, scrape_general, stream_openai, video_openai, double_arrow, use_hinting, image_series 
    #global model_class, prompt_strategy
    #global smaller, make_corpus, corpus_offset, temperature, top_p 

    parser = argparse.ArgumentParser(description='Pong for llm')
    parser.add_argument('--generate', action='store_true', help='Use chat or generate. Chat is default.')
    parser.add_argument('--no_opponent', action='store_true', help='Computer opponent or adversary.')
    parser.add_argument('--key_input', action='store_true', help='Dis-allow text input so LLM can not control one player.')
    parser.add_argument('--small_test', default=-1, type=int, help='Set small_test variable to integer value.')
    parser.add_argument('--sudden_death', default=-1, type=int, help='Set a sudden_death_score to integer value.')
    parser.add_argument('--model', default='qwen3-vl:2b', type=str, help='Set model for local LLMs. default is "qwen3-vl:2b"')
    parser.add_argument('--skip', default=4, type=int, help='Number of computer iterations to skip for each call to the LLM.')
    parser.add_argument('--q_len', default=3, type=int, help="Set queue length for video images.")
    parser.add_argument('--context_size', default=4096, type=int, help="Set context_size for memory.")
    parser.add_argument('--thinking', action='store_true', help="Do not disable thinking mode.")
    parser.add_argument('--threshold', default=75, type=int, help="Threshold for opponent to respond to ball - 1 to 100")
    parser.add_argument('--image_strip', default=-1, type=int, help="Enable comic strip type image manipulation.")
    parser.add_argument('--no_llm', default=-1, type=int, help="Run for specified number of iterations without LLM.")
    parser.add_argument('--stream', action='store_true', help="Access model in Stream mode.")
    parser.add_argument('--stream_openai', action='store_true', help="Use OpenAI format and OpenAI endpoint. Only uses stream and chat.")
    parser.add_argument('--video_openai', action='store_true', help="Use video format in the OpenAI code. Must set image_strip to -1.")
    parser.add_argument('--scrape_general', action='store_true', help="Scrape output for simple commands.")
    parser.add_argument('--double_arrow', action='store_true', help="Include double_arrow with ball position and ball movement.")
    parser.add_argument('--hinting', action='store_true', help="Use ball direction hinting to help the AI.")
    parser.add_argument('--image_series', action='store_true', help="Save png images for later video manipulation.")
    parser.add_argument('--strategy', default=3, type=int, help="Set prompt strategy. Use '1' - '3'. Default is '3'.")
    parser.add_argument('--inverse_size', default=4, type=int, help="Set inverse size adjustment. Use '1' '2' or '4'.")
    parser.add_argument('--make_corpus', default=-1, type=int, help="Make training corpus. (Try 1000?)")
    parser.add_argument('--corpus_offset', default=0, type=int, help="Offset number for the make_corpus functionality. (Default 0)")
    parser.add_argument('--temperature', default=-1, type=float, help="Set the temperature.")
    parser.add_argument('--top_p', default=-1, type=float, help="Set top_p. Use '0.0' to '1.0'. (Default 1.0)")
    args = parser.parse_args()
    if args.generate:
        plugin_class.use_chat = not args.generate 
    if args.no_opponent:
        plugin_class.auto = not args.no_opponent
    if args.key_input:
        plugin_class.text_input = not args.key_input
    if args.small_test >= -1:
        plugin_class.small_test = args.small_test
    if args.sudden_death >= -1:
        plugin_class.sudden_death_score = args.sudden_death
    if len(args.model) > 0:
        plugin_class.model = args.model
        #model = 'gpt-5.2'
    if args.skip >= -1:
        plugin_class.skip = args.skip
    if args.q_len >= -1:
        plugin_class.queue_len = args.q_len
    if args.context_size >= -1:
        plugin_class.context_size = args.context_size
    if args.thinking:
        plugin_class.disable_thinking = not args.thinking
    if args.threshold > 0:
        plugin_class.random_threshold = args.threshold
    if args.image_strip > -1:
        plugin_class.image_strip = args.image_strip
    if args.no_llm > 0:
        plugin_class.no_llm = args.no_llm - 1
    if args.stream:
        plugin_class.stream_requests = args.stream 
    if args.scrape_general:
        plugin_class.scrape_general = args.scrape_general
    if args.stream_openai:
        plugin_class.stream_openai = args.stream_openai
    if args.video_openai:
        plugin_class.video_openai = args.video_openai 
    if args.double_arrow:
        plugin_class.double_arrow = args.double_arrow
    if args.hinting:
        plugin_class.use_hinting = args.hinting
    if args.image_series:
        plugin_class.image_series = args.image_series
    if args.strategy > 0:
        plugin_class.prompt_strategy = args.strategy
    if args.inverse_size > 0:
        plugin_class.smaller = args.inverse_size
    if args.make_corpus > 0:
        plugin_class.make_corpus = args.make_corpus
        plugin_class.no_llm = args.make_corpus
    if args.corpus_offset > -1:
        plugin_class.corpus_offset = args.corpus_offset
    if args.temperature > -1:
        plugin_class.temperature = args.temperature
    if args.top_p > -1:
        plugin_class.top_p = args.top_p

    plugin_class.size_init()

    return

    if  plugin_class.no_llm <= 0 or plugin_class.make_corpus > -1:
        if model not in whitelist:
            print('model not in whitelist')
            sys.exit()

        model_key = ''
        if whitelist[model] == 'Oai':
            model_key = os.getenv('OPENAI_API_KEY')
        if whitelist[model] == 'Gem':
            model_key = os.getenv('GEMINI_API_KEY')
        if whitelist[model] == 'Mis':
            model_key = os.getenv('MISTRAL_API_KEY')
        
        if model in whitelist:
            modelname = whitelist[model]
        else:
            modelname = model

        model_class = globals()[modelname](model, streaming=stream_requests, chat=use_chat, visual=True, think=not disable_thinking, key=model_key)
        model_class.images_size = queue_len 
        model_class.context_size = context_size
        model_class.history_size = context_size 
        model_class.temperature = temperature
        model_class.top_p = top_p
        #model_class.print_to_screen = True
    #####
        if image_strip > 0 and not video_openai :
            model_class.images_size = 1 

   

def scrape(xx, side_effects=True):
    global paddle2_vel, vel_const, skip, vel_const_right

    xx_up = xx.rfind('control.move.up')
    xx_down = xx.rfind('control.move.down')
    
    #paddle2_vel = 0
    paddle = 0 
    #print(xx_up, xx_down)

    if xx_up != -1 and xx_up > xx_down:
        paddle = - self.vel_const_right * skip
        xx = 'control.move.up'
    if xx_down != -1 and xx_down > xx_up :
        paddle = self.vel_const_right * skip
        xx = 'control.move.down'
    if (not 'control.move.up' in xx) and (not 'control.move.down' in xx):
        if scrape_general:
            xx_up = xx.rfind('up')
            xx_down = xx.rfind('down')
            if xx_up != -1 and xx_up > xx_down:
                paddle = - self.vel_const_right * skip
                xx = 'control.move.up'
            if xx_down != -1 and xx_down > xx_up :
                paddle = self.vel_const_right * skip
                xx = 'control.move.down'
            if (not 'up' in xx) and (not 'down' in xx):
                paddle = 0 
                print('NO ANSWER', xx)
                xx = 'control.move.wait'
        else:
            paddle = 0
            if not 'control.move.wait' in xx:
                print('NO ANSWER', xx)
            xx = 'control.move.wait'

    if side_effects:
        paddle2_vel = paddle 

    return xx 

def remove(output, control):
    xx_control = output.rfind(control)
    if xx_control > -1:
        output = output[: xx_control] + output[xx_control + len(control): ]
    return output

#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_UP:
        paddle2_vel = - self.vel_const
    elif event.key == K_DOWN:
        paddle2_vel = self.vel_const
    elif event.key == K_w and not auto:
        paddle1_vel = - self.vel_const
    elif event.key == K_s and not auto:
        paddle1_vel = self.vel_const

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

if __name__ == "__main__":

    plugin_class = PygamePongAgent()
    parse()
    plugin_class.init() 
    try:
        #game loop
        plugin_class.step_count = 0 
        num = 0
        er = 0
        last_code = 200 
        while True:
            plugin_class.window = pygame.display.set_mode((plugin_class.WIDTH, plugin_class.HEIGHT))

            plugin_class.draw(plugin_class.window)

            if not plugin_class.text_input:
                for event in pygame.event.get():

                    if event.type == KEYDOWN:
                        keydown(event)
                    elif event.type == KEYUP:
                        keyup(event)
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        sys.exit()

                if num % plugin_class.skip == 0 or len(plugin_class.message) > 0:  
                    m = plugin_class.make_message()
                    if plugin_class.small_test > -1 :
                        img = num // plugin_class.skip 
                        p = plugin_class.prompt_list[img % len(plugin_class.prompt_list)]
                        if not plugin_class.stream_openai:
                            m = p + ' - ' + m 
                        else:
                            m = plugin_class.prompt_list[0] 
                    else:
                        img = 0

                    if plugin_class.image_series or plugin_class.make_corpus > 0:
                        img = ('00000000000' + str(plugin_class.step_count + plugin_class.corpus_offset))[- 10:]
                        print(img)
                    f = './pic/figure_' + str(img) + '.png'
                    
                    if plugin_class.make_corpus > 0:
                        f = './pic/' + str(img) + '.png'

                    if plugin_class.no_llm > 0 and plugin_class.step_count  >= plugin_class.no_llm :
                        #print('exit before png save')
                        sys.exit()

                    plugin_class.pygame_save(f)

                    if int(img) > plugin_class.small_test and plugin_class.small_test > -1 and not plugin_class.stream_openai :
                        sys.exit()

                    z = plugin_class.encode_image_to_base64(f)
                    
                    # open in the system browser!!
                    #subprocess.run(['open','data:image/png;base64,' + z])
                    #sys.exit()

                    print(m + '\n---')

                    if plugin_class.no_llm <= -1:
                        xx = model_class.do(image=z, context=None, text=m )
                    if plugin_class.no_llm > 0 and plugin_class.step_count > plugin_class.no_llm :
                        sys.exit()
                    elif plugin_class.no_llm > 0:
                        pygame.display.update()
                        ticks = 15
                        plugin_class.fps.tick(ticks)
                        if plugin_class.make_corpus > 0:
                            #model_class.print_to_screen = True
                            x = model_class.do(image=z, context=None, text=m)
                            xx = scrape(x, side_effects=False)
                            x = remove(x, xx)
                            model_class.write(scraped_output=paddle_message, raw_output=x, raw_input=m, num_string=img)
                            paddle_message = ''

                        plugin_class.step_count += 1 
                        continue

                    print(xx)
                    xx = scrape(xx)

                    if len(plugin_class.message) > 0:
                        plugin_class.commands.append(xx + ' --' + str(plugin_class.message) + '--')
                    else:
                        plugin_class.commands.append(xx)
                    print('[' + str(plugin_class.step_count + 1) + ']', xx)

                    #print('ball_vel', ball_vel, 'ball_pos', ball_pos)
                    
                    plugin_class.step_count += 1
                    plugin_class.message = ''
                    plugin_class.stats(True)

                    
                    if plugin_class.step_count >= plugin_class.small_test and plugin_class.small_test > -1 and plugin_class.stream_openai :
                        sys.exit()

                    if plugin_class.sudden_death_score != -1 and (plugin_class.l_score >= plugin_class.sudden_death_score or plugin_class.r_score >= plugin_class.sudden_death_score):
                        print('sudden_death_score', plugin_class.l_score, plugin_class.r_score)
                        if plugin_class.make_corpus > 0:
                            plugin_class.l_score = 0 
                            plugin_class.r_score = 0
                            
                        else:    
                            sys.exit()

                num += 1  

            pygame.display.update()
            ticks = 60
            plugin_class.fps.tick(ticks)

    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')

    finally:
        print('---')
        plugin_class.stats(False)
        pass 
        


