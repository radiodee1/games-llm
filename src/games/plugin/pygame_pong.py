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
from plugin import DefaultBare
#from query import  Oai, Ollama, Gem, Mis 

class PygamePongAgent(DefaultBare):

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

        self.action_meaning = [
            {
                'name': 'control.move.wait',
                'num': 0,
                'meaning': 'control.move.wait'
            },
            {
                'name': 'control.move.up',
                'num': 1,
                'meaning': 'control.move.up'

            },
            {
                'name': 'control.move.down',
                'num': 2,
                'meaning': 'control.move.down'

            }
        ]
        
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


    # helper function that spawns a ball, returns a position vector and a velocity vector
    # if right is True, spawn to the right, else spawn to the left
    def ball_init(self, right):
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
    def draw(self, canvas=None):
        if canvas == None:
            canvas = self.window
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
        vx, vy = self.ball_vel
        if vx == 0:
            vx = 0.01
        m = vy / vx 
        b = self.ball_pos[1] - m * self.ball_pos[0] 
        hint_y = m * ( self.WIDTH - self.PAD_WIDTH ) + b 
        return int(hint_y)

    def is_hint_now(self, hint_y):
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

        r = r + title + ' - ' + score + ' - ' + controls +  ' AI must use the picture and reply to play the game!' + ' ' + limit
        return r 

    def stats(self, short=True):
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

    def image_save(self, filename):
        self.pygame_save(filename)

    def pygame_save(self, f):
        print(f)
        border_rect = pygame.Surface((self.WIDTH + 2 * self.BORDER_SIZE, self.HEIGHT + 2 * self.BORDER_SIZE))
        border_rect.fill(self.GRAY)
        border_rect.blit(self.window, (self.BORDER_SIZE, self.BORDER_SIZE))


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
            ii = 0 
            for i in self.strip:
                if self.image_strip > 1:
                    i = self.label(i, ii + 0) 
                window_strip.blit(i, ((self.WIDTH + 2 * self.BORDER_SIZE) * ii, 0))
                ii += 1 
            
            pygame.image.save(window_strip, f)

    def scrape(self, txt, replace=False):
        txt = super().scrape(txt, replace)
        if self.action_string == 'control.move.up':
            self.paddle2_vel = - self.vel_const_right #* self.skip
        if self.action_string == 'control.move.down':
            self.paddle2_vel = self.vel_const_right #* self.skip
        if self.action_string == 'control.move.wait':
            self.paddle2_vel = 0 
        #print('paddle2_vel:', self.paddle2_vel , 'vel_const_right', self.vel_const_right )

        return txt 


if __name__ == "__main__":
    pass 

