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
from plugin import DefaultBare, PygamePongAgent, LunarLanderAgent, PongAgent
from query import  Oai, Ollama, Gem, Mis 

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

pluginlist = {
    'lunarlander'       : 'LunarLanderAgent',
    'pong'              : 'PongAgent'
}

plugin_class = None
pluginname = ''
pluginraw = ''

def parse():
    global model_class, plugin_class, pluginname, pluginraw 

    parser = argparse.ArgumentParser(description='Games for llm')
    parser.add_argument('--plugin', default='', type=str, help='Game plugin for tests.')
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

    pluginname = ''
    if len(args.plugin) > 0:
        pluginraw = args.plugin 
        if args.plugin in pluginlist:
            pluginname = pluginlist[args.plugin]
            plugin_class = globals()[pluginname]()


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
        model = args.model 
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

    if not args.plugin in pluginlist:
        plugin_class.size_init()

    #return

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

        model_class = globals()[modelname](model, streaming=plugin_class.stream_requests, chat=plugin_class.use_chat, visual=True, think=not plugin_class.disable_thinking, key=model_key)
        model_class.images_size = plugin_class.queue_len 
        model_class.context_size = plugin_class.context_size
        model_class.history_size = plugin_class.context_size 
        model_class.temperature = plugin_class.temperature
        model_class.top_p = plugin_class.top_p
        
        model_class.print_to_screen = True
        
        if plugin_class.image_strip > 0 and not plugin_class.video_openai :
            model_class.images_size = 1 

   

def scrape(xx, side_effects=True):

    xx_up = xx.rfind('control.move.up')
    xx_down = xx.rfind('control.move.down')
    
    #paddle2_vel = 0
    paddle = 0 
    #print(xx_up, xx_down)
    skip = plugin_class.skip
    vel_const_right = plugin_class.vel_const_right

    if xx_up != -1 and xx_up > xx_down:
        paddle = - vel_const_right * skip
        xx = 'control.move.up'
    if xx_down != -1 and xx_down > xx_up :
        paddle = vel_const_right * skip
        xx = 'control.move.down'
    if (not 'control.move.up' in xx) and (not 'control.move.down' in xx):
        if plugin_class.scrape_general:
            xx_up = xx.rfind('up')
            xx_down = xx.rfind('down')
            if xx_up != -1 and xx_up > xx_down:
                paddle = - vel_const_right * skip
                xx = 'control.move.up'
            if xx_down != -1 and xx_down > xx_up :
                paddle = vel_const_right * skip
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
        plugin_class.paddle2_vel = paddle 

    return xx 

def remove(output, control):
    xx_control = output.rfind(control)
    if xx_control > -1:
        output = output[: xx_control] + output[xx_control + len(control): ]
    return output

#keydown handler
def keydown(event):

    vel_const = plugin_class.vel_const

    if event.key == K_UP:
        plugin_class.paddle2_vel = - vel_const
    elif event.key == K_DOWN:
        plugin_class.paddle2_vel = vel_const
    elif event.key == K_w and not plugin_class.auto:
        plugin_class.paddle1_vel = - vel_const
    elif event.key == K_s and not plugin_class.auto:
        plugin_class.paddle1_vel = vel_const

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
    plugin_class.reset()
    plugin_class.fps = pygame.time.Clock()
    try:
        #game loop
        plugin_class.step_count = 0 
        num = 0
        er = 0
        last_code = 200 
        while True:
            if not pluginraw in pluginlist:
                plugin_class.window = pygame.display.set_mode((plugin_class.WIDTH, plugin_class.HEIGHT))
            else:
                plugin_class.action = plugin_class.env.action_space.sample()
                print(plugin_class.action)

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

                    #plugin_class.pygame_save(f)
                    plugin_class.image_save(f)

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
                        if not pluginraw in pluginlist:
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

                    if plugin_class.truncated or plugin_class.terminated:
                        plugin_class.reset()


                    if plugin_class.sudden_death_score != -1 and (plugin_class.l_score >= plugin_class.sudden_death_score or plugin_class.r_score >= plugin_class.sudden_death_score):
                        print('sudden_death_score', plugin_class.l_score, plugin_class.r_score)
                        if plugin_class.make_corpus > 0:
                            plugin_class.l_score = 0 
                            plugin_class.r_score = 0
                            
                        else:    
                            sys.exit()

                num += 1  

            if not pluginraw in pluginlist:
                pygame.display.update()

            ticks = 60
            plugin_class.fps.tick(ticks)

    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')

    finally:
        print('---')
        plugin_class.stats(False)
        pass 
        


