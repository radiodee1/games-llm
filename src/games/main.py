#!/usr/bin/env python3

#PONG pygame

import json
import random
import pygame, sys
from pygame.locals import *
import os 
import time
import requests
import base64
import argparse 
import math
from query import  Oai, Ollama, Gem

from dotenv import load_dotenv 

load_dotenv()

pygame.init()
fps = pygame.time.Clock()
start_time = time.perf_counter()

#size adjustment
smaller = 4 

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (10,10,10)
GRAY = (100,100,100)
BLUE = (0,0,255)

#globals
WIDTH = 600 // smaller
HEIGHT = 400 // smaller      
BALL_RADIUS = 20 // smaller
PAD_WIDTH = 16 // smaller
PAD_HEIGHT = 80 // smaller
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_pos = [0,0]
paddle2_pos = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
trace_pos = [0,0] 
paddle1_bounce = 0 
paddle2_bounce = 0
serves_num = 0 

BORDER_SIZE = 24 // smaller

auto = True
text_input = True
small_test = -1 ## set to -1 for 'no test'
vel_const = 8 // smaller
vel_const_right = 4 // smaller # 16!
skip = 4
num = 0 
message = ''
fontsize = 48 // smaller
LOCAL_LLM = 'http://localhost:11434/api/'

prompt_list = ['Describe the arrow in this picture. What direction is it pointing? What is its up/down angle?' , 
               'My name is David.', 
               'What is my name?', 
               'What is your favorate color?' ]

acceleration = .25
sudden_death_score = -1
disable_thinking = True
context_size = 4096
use_chat = True
queue_len = 4 
commands = []
random_threshold = 50
no_llm = -1 
image_strip = -1 
strip = []
stream_requests = False
stream_openai = False 
timeout = 600 # implement me!!
scrape_general = False
video_openai = False
double_arrow = False
use_hinting = False
image_series = False
prompt_strategy = 1 
make_corpus = -1

arrow_surface = None ## for arrow...

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
    'gemini-2.5-flash'       : 'Gem'
}

pygame.display.set_caption('Pong')

def size_init():

    global WIDTH, HEIGHT, BALL_RADIUS, PAD_WIDTH, PAD_HEIGHT, HALF_PAD_WIDTH, HALF_PAD_HEIGHT, BORDER_SIZE
    global vel_const, vel_const_right, fontsize, smaller 
    
    print('smaller' ,smaller)
    WIDTH = 600 // smaller
    HEIGHT = 400 // smaller      
    BALL_RADIUS = 20 // smaller
    PAD_WIDTH = 16 // smaller
    PAD_HEIGHT = 80 // smaller
    HALF_PAD_WIDTH = PAD_WIDTH // 2
    HALF_PAD_HEIGHT = PAD_HEIGHT // 2
    BORDER_SIZE = 24 // smaller
    vel_const = 8 // smaller
    vel_const_right = 4 // smaller # 16!
    fontsize = 48 // smaller


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    global serves_num, message

    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]
    serves_num += 1 
    message += "Serve!!"

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2, arrow_surface  
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)
    arrow_surface = draw_arrow() 

#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
    global message, num, skip, trace_pos, paddle1_bounce, paddle2_bounce, random_threshold 
    global make_corpus

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70 // smaller, 1)

    # update paddle's vertical position, keep paddle on the screen
    if make_corpus < 0:
        computer = random.random() 
        if not auto:
            if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
                paddle1_pos[1] += paddle1_vel
            elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
                paddle1_pos[1] += paddle1_vel
            elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
                paddle1_pos[1] += paddle1_vel
        if auto and num % skip == 0 and computer <= random_threshold / 100:
            if paddle1_pos[1] >= int(ball_pos[1]) and ball_vel[1] < 0:  
                paddle1_pos[1] -= abs(vel_const) * skip # up - negative 
                print('computer paddle up', - abs(vel_const) * skip)
            elif paddle1_pos[1] <= int(ball_pos[1]) and ball_vel[1] > 0:  
                paddle1_pos[1] += abs(vel_const) * skip # down - positive
                print('computer paddle down', abs(vel_const) * skip)
        elif auto and num % skip == 0:
            print('pass because of threshold', computer * 100)

        if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            paddle2_pos[1] += int(paddle2_vel)
        if paddle2_pos[1] < HALF_PAD_HEIGHT + int(paddle2_vel) and int(paddle2_vel) > 0:
            paddle2_pos[1] += int(paddle2_vel)
        if paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT - int(paddle2_vel) and int(paddle2_vel) < 0:
            paddle2_pos[1] += int(paddle2_vel)

        if paddle2_pos[1] <= HALF_PAD_HEIGHT  and int(paddle2_vel) > 0:
            paddle2_pos[1] += int(paddle2_vel)
        if paddle2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT and int(paddle2_vel) < 0:
            paddle2_pos[1] += int(paddle2_vel)

    elif make_corpus > 0 and num % skip == 0 :
        paddle2_message = ''
        temp1_vel, paddle1_message = paddle_auto_vel(paddle1_pos, ball_pos, ball_vel, vel_const)
        paddle1_pos[1] += temp1_vel * skip 
        temp2_vel, paddle2_message = paddle_auto_vel(paddle2_pos, ball_pos, ball_vel, vel_const_right)
        paddle2_pos[1] += temp2_vel * skip
        print( paddle1_pos, paddle1_message, paddle2_pos, 'paddles', paddle2_message, vel_const, vel_const_right )

    if num % skip == 0:
        trace_pos[0] = ball_pos[0] - ball_vel[0] * ( 4 // smaller )  
        trace_pos[1] = ball_pos[1] - ball_vel[1] * ( 4 // smaller )

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    if not double_arrow:
        pygame.draw.circle(canvas, GRAY, trace_pos, BALL_RADIUS, 0)
    blit_rotate_arrow(canvas, arrow_surface, ball_pos, ball_vel)
    pygame.draw.circle(canvas, RED, ball_pos, BALL_RADIUS, 0)
    paddle1_points = [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]]
    paddle2_points = [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]]
    
    pygame.draw.polygon(canvas, GREEN, paddle1_points, 0)
    pygame.draw.polygon(canvas, GREEN, paddle2_points, 0)
    
    stripe_polygon(canvas, paddle1_points, WHITE, 8 // smaller, 16 // smaller)
    stripe_polygon(canvas, paddle2_points, BLUE, 8 // smaller, 16 // smaller)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        message = "Bounce!!"
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        message = "Bounce!!"
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(int(paddle1_pos[1]) - HALF_PAD_HEIGHT, int(paddle1_pos[1]) + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= (1.0 + acceleration)
        ball_vel[1] *= (1.0 + acceleration)
        paddle1_bounce += 1 
        message = "Uh oh!!"
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        message = "Score!!"
        ball_init(True)
        
    if int(ball_pos[0]) > WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) > int(paddle2_pos[1]) - HALF_PAD_HEIGHT and int(ball_pos[1]) < int(paddle2_pos[1]) + HALF_PAD_HEIGHT:  
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= (1.0 + acceleration)
        ball_vel[1] *= (1.0 + acceleration)
        paddle2_bounce += 1 
        message = "Nice!!"
    elif int(ball_pos[0]) > WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        message = "Ouch!!"
        ball_init(False)
    
    if use_hinting:
        hint_x = WIDTH - PAD_WIDTH
        hint_y = get_hint_y() 
        if is_hint_now(hint_y):
            pygame.draw.line(canvas, RED, (hint_x, hint_y), (hint_x + 2, hint_y), 8)

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", fontsize)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50 // smaller,20 // smaller))

    myfont2 = pygame.font.SysFont("Comic Sans MS", fontsize)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (410 // smaller, 20 // smaller)) 

    pygame.display.update([canvas.get_rect()])

def stripe_polygon(canvas, polygon, color, width, seperation):
    ul, ur, lr, ll = polygon
    slant = 0 # 4 
    x1, y1 = ul
    x2, y2 = lr 
    for i in range(y1, y2, seperation + width):
        pygame.draw.line(canvas, color, (x1, i), (x2, i + slant), width )
    pass 

def draw_arrow():
    global double_arrow, smaller
    # -->
    xoffset = 100 # // smaller # 25 ## 35! 
    arrow_lines = [
        (BLUE, (160, 0),   (200, 20), 8 // smaller  ),  # angle line
        (BLUE, (120, 20),  (200, 20), 8 // smaller  ),  # horizontal line
        (BLUE, (160, 48),  (200, 20), 8 // smaller  ),  # angle line
    ]
    arrow_surface = pygame.Surface((400 // smaller, 48 // smaller), pygame.SRCALPHA)
    xoffset = 100 # // smaller # 25 
    for color, start_pos, end_pos, width in arrow_lines:
        start_pos = (start_pos[0]  + xoffset) // smaller , start_pos[1] // smaller
        end_pos = (end_pos[0]  + xoffset) // smaller, end_pos[1] // smaller
        pygame.draw.line(arrow_surface, color, start_pos, end_pos, width)
    
    if double_arrow:
        xoffset = - 80 #// smaller #20 
        for color, start_pos, end_pos, width in arrow_lines:
            start_pos = (start_pos[0]  + xoffset) // smaller, start_pos[1] // smaller
            end_pos = (end_pos[0]  + xoffset) // smaller, end_pos[1] // smaller
            pygame.draw.line(arrow_surface, color, start_pos, end_pos, width)
    return arrow_surface

def blit_rotate_arrow(surf, image, center,  ball_vel):
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

def get_hint_y():
    global ball_pos, ball_vel 
    vx, vy = ball_vel
    if vx == 0:
        vx = 0.01
    m = vy / vx 
    b = ball_pos[1] - m * ball_pos[0] 
    hint_y = m * ( WIDTH - PAD_WIDTH ) + b 
    print('hint_y', hint_y)
    return int(hint_y)

def is_hint_now(hint_y):
    global ball_pos, ball_vel, paddle2_pos  
    is_facing_right = False
    if ball_vel[0] > 0:
        is_facing_right = True
    if paddle2_pos[1] - HALF_PAD_HEIGHT < hint_y and paddle2_pos[1] + HALF_PAD_HEIGHT > hint_y and is_facing_right:
        return True
    else:
        return False

def paddle_auto_vel(paddle_pos, ball_pos, ball_vel, vel_const=2):
    if paddle_pos[0] < WIDTH // 2:
        #left 
        if paddle_pos[1] >= int(ball_pos[1]) and ball_vel[1] < 0:  
            return (- abs(vel_const) , 'control.move.up' )  # up - negative 
        elif paddle_pos[1] <= int(ball_pos[1]) and ball_vel[1] > 0:  
            return (+ abs(vel_const) , 'control.move.down') # down - positive
        return (0, 'control.move.wait')
    else:
        #right 
        i = get_hint_y()
        if i < 0 or i > HEIGHT:
            return (0 , 'control.move.wait')
        if i > paddle_pos[1] - HALF_PAD_HEIGHT and i < paddle_pos[1] + HALF_PAD_HEIGHT:
            return (0 , 'control.move.wait')
        if paddle_pos[1] >= i: # and ball_vel[1] < 0:
            return (- abs(vel_const), 'control.move.up')
        elif paddle_pos[1] <= i: # and ball_vel[1] > 0:
            return (+ abs(vel_const), 'control.move.down')
        return(0, 'control.move.wait')
    pass 

def label(i, ii):
    myfont = pygame.font.SysFont(None, 16 )
    label1 = myfont.render("# " + str(ii), True, (255,255,0), GRAY)
    label1_rect = label1.get_rect();
    label1_rect.center = (WIDTH // 2 + BORDER_SIZE , int(HEIGHT + BORDER_SIZE - 2) )
    i.blit(label1, label1_rect )
    return i 

def make_message():
    global l_score, r_score, message, commands, prompt_strategy
    if use_hinting:
        hint_y = get_hint_y()

    title = 'Turn-based Pong or Tennis game. AI vs computer.'
    old_controls = (
                ' Estimate the angle of the ball from the arrow and move your paddle to the position where you can hit the ball back to the other side.\n'
                ' Enter "control.move.up" or "control.move.down" to move the Paddle in anticipation of the ball.'  
                ' The paddle only moves up and down.'
                ' Enter "control.move.wait" to skip one turn.'        
                ' The ball is red. The ball is moving in the direction of the arrow. The arrow is blue.'                
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
    control_list = [ old_controls, new_controls ]

    controls = control_list[ prompt_strategy - 1 ]

    controls += ('NOTE:\n'
                ' Your paddle is blue and green. It is very small.\n'
                ' The paddle only moves up and down.\n'
                ' Enter "control.move.wait" to skip one turn.\n'        
                ' The ball is red. The ball is moving in the direction of the arrow. The arrow is blue.\n'  
                ' The left paddle moves on its own.\n'
                ' Hit the ball when it comes to you.\n'
                ' This is the only way to win.\n')

    score = 'Their score ' + str(l_score) + ' / Your score ' + str(r_score) + ' - Left Bounces ' + str(paddle1_bounce) + ' / Right Bounces ' + str(paddle2_bounce)
    
    # limit = 'Answer in one line under 20 characters.'
    
    limit = 'Show your thinking and then reply with your final answer.'
    hint = ' Hint: Wait right there!'
    r = ''
    if use_hinting and is_hint_now(hint_y):
        controls += hint 
    if disable_thinking:
        limit = limit + ' Do not use thinking.'
    if len(message) > 0:
        r = message + ' - '
        #commands.append(str('--' + message + '--')) ## keep array size the same as step_count

    r = r + title + ' - ' + score + ' - ' + controls +  ' AI must use the picture and reply to play the game!' + ' ' + limit
    return r 

def stats(short=True):
    global paddle1_bounce, paddle2_bounce, l_score, r_score, num, skip, commands, step_count, serves_num 
    global model
    print("model:", model)
    print("serves_num:", serves_num)
    print("Left-bounces:", paddle1_bounce, 'Right-bounces:', paddle2_bounce)
    print("l_score:", l_score, "r_score:", r_score)
    single = 0 
    if not short:
        single = 1 
    print("step-count:", (step_count + single))
    
    end_time = time.perf_counter()
    elapsed_min = (end_time - start_time) // 60 
    elapsed_sec = (end_time - start_time) - elapsed_min * 60
    elapsed_sec = '0000' + str(int(elapsed_sec))
    elapsed_sec = elapsed_sec[-2:]
    print(f"Elapsed time: {elapsed_min:.0f}:{elapsed_sec} minutes")
    print('---')
    if short:
        return
    num = 0 
    for i in commands:
        print(num + 1, i)
        num += 1 

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def parse():
    global use_chat, auto, text_input, small_test, sudden_death_score, model, skip, smaller 
    global LOCAL_LLM, queue_len, context_size, disable_thinking, random_threshold, image_strip, no_llm
    global stream_requests, scrape_general, stream_openai, video_openai, double_arrow, use_hinting, image_series 
    global model_class, prompt_strategy
    global smaller, make_corpus 

    parser = argparse.ArgumentParser(description='Pong for llm')
    parser.add_argument('--generate', action='store_true', help='Use chat or generate. Chat is default.')
    parser.add_argument('--no_opponent', action='store_true', help='Computer opponent or adversary.')
    parser.add_argument('--key_input', action='store_true', help='Dis-allow text input so LLM can not control one player.')
    parser.add_argument('--small_test', default=-1, type=int, help='Set small_test variable to integer value.')
    parser.add_argument('--sudden_death', default=-1, type=int, help='Set a sudden_death_score to integer value.')
    parser.add_argument('--model', default='qwen3-vl:2b', type=str, help='Set model for local LLMs. default is "qwen3-vl:2b"')
    parser.add_argument('--skip', default=4, type=int, help='Number of computer iterations to skip for each call to the LLM.')
    parser.add_argument('--compress', default=4, type=int, help='Set "smaller" to number that will compress screen size.')
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
    parser.add_argument('--strategy', default=1, type=int, help="Set prompt strategy. Use '1' or '2'.")
    parser.add_argument('--inverse_size', default=4, type=int, help="Set inverse size adjustment. Use '1' '2' or '4'.")
    parser.add_argument('--make_corpus', default=-1, type=int, help="Make training corpus. (Try 1000?)")
    args = parser.parse_args()
    if args.generate:
        use_chat = not args.generate 
    if args.no_opponent:
        auto = not args.no_opponent
    if args.key_input:
        text_input = not args.key_input
    if args.small_test >= -1:
        small_test = args.small_test
    if args.sudden_death >= -1:
        sudden_death_score = args.sudden_death
    if len(args.model) > 0:
        model = args.model
        #model = 'gpt-5.2'
    if args.skip >= -1:
        skip = args.skip
    if args.compress >= -1:
        smaller = args.compress
    if args.q_len >= -1:
        queue_len = args.q_len
    if args.context_size >= -1:
        context_size = args.context_size
    if args.thinking:
        disable_thinking = not args.thinking
    if args.threshold > 0:
        random_threshold = args.threshold
    if args.image_strip > -1:
        image_strip = args.image_strip
    if args.no_llm > 0:
        no_llm = args.no_llm - 1
    if args.stream:
        stream_requests = args.stream 
    if args.scrape_general:
        scrape_general = args.scrape_general
    if args.stream_openai:
        stream_openai = args.stream_openai
    if args.video_openai:
        video_openai = args.video_openai 
    if args.double_arrow:
        double_arrow = args.double_arrow
    if args.hinting:
        use_hinting = args.hinting
    if args.image_series:
        image_series = args.image_series
    if args.strategy > 0:
        prompt_strategy = args.strategy
    if args.inverse_size > 0:
        smaller = args.inverse_size
    if args.make_corpus > 0:
        make_corpus = args.make_corpus
        no_llm = args.make_corpus

    size_init()

    if  no_llm <= 0 or make_corpus > -1:
        if model not in whitelist:
            print('model not in whitelist')
            sys.exit()
        
        model_key = os.getenv('OPENAI_API_KEY')
        if whitelist[model] == 'Gem':
            model_key = os.getenv('GEMINI_API_KEY')

        model_class = globals()[whitelist[model]](model, streaming=stream_requests, chat=use_chat, visual=True, think=False, key=model_key)
        model_class.images_size = queue_len 
        model_class.context_size = context_size
        model_class.history_size = context_size 
        if make_corpus > 0:
            model_class.write_only = True
    #####
        if image_strip > 0 and not video_openai :
            model_class.images_size = 1 

   

def scrape(xx):
    global paddle2_vel, vel_const, skip, vel_const_right

    xx_up = xx.rfind('control.move.up')
    xx_down = xx.rfind('control.move.down')
    
    paddle2_vel = 0 
    #print(xx_up, xx_down)

    if xx_up != -1 and xx_up > xx_down:
        paddle2_vel = - vel_const_right * skip
        xx = 'control.move.up'
    if xx_down != -1 and xx_down > xx_up :
        paddle2_vel = vel_const_right * skip
        xx = 'control.move.down'
    if (not 'control.move.up' in xx) and (not 'control.move.down' in xx):
        if scrape_general:
            xx_up = xx.rfind('up')
            xx_down = xx.rfind('down')
            if xx_up != -1 and xx_up > xx_down:
                paddle2_vel = - vel_const_right * skip
                xx = 'control.move.up'
            if xx_down != -1 and xx_down > xx_up :
                paddle2_vel = vel_const_right * skip
                xx = 'control.move.down'
            if (not 'up' in xx) and (not 'down' in xx):
                paddle2_vel = 0 
                print('NO ANSWER', xx)
                xx = 'control.move.wait'
        else:
            paddle2_vel = 0
            if not 'control.move.wait' in xx:
                print('NO ANSWER', xx)
            xx = 'control.move.wait'

    return xx 


#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_UP:
        paddle2_vel = - vel_const
    elif event.key == K_DOWN:
        paddle2_vel = vel_const
    elif event.key == K_w and not auto:
        paddle1_vel = - vel_const
    elif event.key == K_s and not auto:
        paddle1_vel = vel_const

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

if __name__ == "__main__":

    parse()
    init()
    try:
        #game loop
        step_count = 0 
        num = 0
        er = 0
        last_code = 200 
        while True:
            window = pygame.display.set_mode((WIDTH, HEIGHT))

            draw(window)

            if not text_input:
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

                if num % skip == 0 or len(message) > 0:  
                    m = make_message()
                    if small_test > -1 :
                        img = num // skip
                        p = prompt_list[img % len(prompt_list)]
                        if not stream_openai:
                            m = p + ' - ' + m 
                        else:
                            m = prompt_list[0] 
                    else:
                        img = 0

                    if image_series:
                        img = ('00000000000' + str(step_count))[- 10:]
                        print(img)
                    f = './pic/figure_' + str(img) + '.png'
                    
                    print(f)
                    border_rect = pygame.Surface((WIDTH + 2 * BORDER_SIZE, HEIGHT + 2 * BORDER_SIZE))
                    border_rect.fill(GRAY)
                    border_rect.blit(window, (BORDER_SIZE, BORDER_SIZE))

                    #pygame.display.update([border_rect.get_rect()])

                    if  image_strip < 0:
                        pygame.image.save(border_rect, f)
                    elif image_strip > 0 :
                        strip.append(border_rect.copy() )
                        i = 0 
                        while len(strip) > image_strip and i < 10:
                            strip.pop(0)
                            print('pop strip img', len(strip))
                            i += 1
                        window_strip = pygame.display.set_mode(( (WIDTH + 2 * BORDER_SIZE) * len(strip) , HEIGHT + 2 * BORDER_SIZE))
                        window_strip.fill(GRAY)
                        #pygame.display.update([window_strip.get_rect()])
                        ii = 0 
                        for i in strip:
                            #pygame.display.update([i.get_rect()])
                            if image_strip > 1:
                                i = label(i, ii + 0) 
                            #pygame.display.update([i.get_rect()])
                            window_strip.blit(i, ((WIDTH + 2 * BORDER_SIZE) * ii, 0))
                            #pygame.display.update([window_strip.get_rect()])
                            ii += 1 
                        pygame.image.save(window_strip, f)
                        #pygame.display.update([window_strip.get_rect()])

                    if int(img) > small_test and small_test > -1 and not stream_openai :
                        sys.exit()

                    z = encode_image_to_base64(f)
                    

                    print(m + '\n---')

                    if no_llm <= -1:
                        xx = model_class.do(image=z, context=None, text=m )
                    if no_llm > 0 and step_count > no_llm:
                        sys.exit()
                    elif no_llm > 0:
                        pygame.display.update()
                        ticks = 15
                        fps.tick(ticks)
                        if make_corpus > 0:
                            #model_class.print_to_screen = True
                            model_class.write()
                        step_count += 1 
                        continue

                    print(xx)
                    xx = scrape(xx)

                    if len(message) > 0:
                        commands.append(xx + ' --' + str(message) + '--')
                    else:
                        commands.append(xx)
                    print('[' + str(step_count + 1) + ']', xx)

                    step_count += 1
                    message = ''
                    stats(True)

                    
                    if step_count >= small_test and small_test > -1 and stream_openai :
                        sys.exit()

                    if sudden_death_score != -1 and (l_score >= sudden_death_score or r_score >= sudden_death_score):
                        print('sudden_death_score', l_score, r_score)
                        sys.exit()

                num += 1  

            pygame.display.update()
            ticks = 60
            fps.tick(ticks)

    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')

    finally:
        print('---')
        stats(False)
        pass 
        


