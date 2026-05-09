#!/usr/bin/env python3

#PONG pygame

#import json
#import random
import pygame, sys
from pygame.locals import *
import os 
#import time
#import subprocess
#import base64
import argparse 
#import math
from GameAgent.game_agent import  PygamePongAgent, LunarLanderAgent, PongAgent, BreakoutAgent
from LLM.llm_do import  Oai, Ollama, Gem, Mis, OllamaImages 

from GameAgent.game_agent import pluginlist, pygamelist
from LLM.llm_do import whitelist

from dotenv import load_dotenv

user_env = os.path.expanduser('~') + '/.llm.env'
load_dotenv(user_env)

#print('GAME_LAUNCH_ARGS' , os.getenv('GAME_LAUNCH_ARGS'))

model = "qwen3-vl:2b"
model_class = None 

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
    parser.add_argument('--video', action='store_true', help="Use video format in the OpenAI code. Must set image_strip to -1.")
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
    parser.add_argument('--no_pic', action='store_true', help="Do not display picture from rom. Useful for gnome.")
    GAME_LAUNCH_ARGS = str(os.getenv('GAME_LAUNCH_ARGS'))
    launch_args = []

    for i in GAME_LAUNCH_ARGS.split(' '):
        if i.strip() != '':
            launch_args.append(i)

    for i in sys.argv[1:]:
        if i.strip() != '':
            launch_args.append(i)

    args = parser.parse_args(launch_args) 


    pluginname = ''
    if len(args.plugin) > 0:
        pluginraw = args.plugin 
        if pluginraw in pluginlist or pluginraw == '':
            pluginname = pluginlist[args.plugin]
            plugin_class = globals()[pluginname](inverse_size=args.inverse_size, show_image=not args.no_pic)
    else:
        print('must specify game agent with --plugin flag. Try "--plugin pong"')
        sys.exit()
    #print(args.plugin ,'show_image', show_image, 'pluginname', pluginname, plugin_class)

    plugin_class.use_chat = not args.generate 
    plugin_class.auto = not args.no_opponent
    plugin_class.text_input = not args.key_input
    plugin_class.small_test = args.small_test
    plugin_class.sudden_death_score = args.sudden_death
    plugin_class.model = args.model
    model = args.model 
    plugin_class.skip = args.skip
    plugin_class.frame_skip = args.skip 
    plugin_class.queue_len = args.q_len
    plugin_class.context_size = args.context_size
    plugin_class.disable_thinking = not args.thinking
    plugin_class.random_threshold = args.threshold
    plugin_class.image_strip = args.image_strip
    plugin_class.no_llm = args.no_llm - 1
    plugin_class.stream_requests = args.stream 
    plugin_class.scrape_general = args.scrape_general
    plugin_class.video = args.video 
    plugin_class.double_arrow = args.double_arrow
    plugin_class.use_hinting = args.hinting
    plugin_class.image_series = args.image_series
    plugin_class.prompt_strategy = args.strategy
    plugin_class.make_corpus = args.make_corpus
    plugin_class.no_llm = args.make_corpus
    plugin_class.corpus_offset = args.corpus_offset
    plugin_class.temperature = args.temperature
    plugin_class.top_p = args.top_p

    plugin_class.repeat_action_probability = 0.0

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
        model_class.history_size = plugin_class.context_size + 1
        model_class.temperature = plugin_class.temperature
        model_class.top_p = plugin_class.top_p
        model_class.smaller = plugin_class.smaller

        #model_class.print_to_screen = True
        model_class.write_to_text = True
        
        if modelname == 'OllamaImages':
            model_class.image_token_budget = 1120

        if plugin_class.image_strip > 0 and not plugin_class.video:
            model_class.images_size = 1 


if __name__ == "__main__":

    #plugin_class = PygamePongAgent()
    parse()

    plugin_class.init()
    plugin_class.reset()
    plugin_class.fps = pygame.time.Clock()

    if pluginraw not in pygamelist and pluginraw != '' and plugin_class.action == None:
        plugin_class.action = plugin_class.env.action_space.sample()

    try:
        #game loop
        plugin_class.step_count = 0 
        num = 0
        er = 0
        last_code = 200 
        while True:
            if pluginraw in pygamelist or pluginraw == '':
                plugin_class.draw()

            if True:

                if num % plugin_class.skip == 0 or len(plugin_class.message) > 0:  
                    if not pluginraw in pygamelist and pluginraw !=  '' :
                        plugin_class.draw()

                    m = plugin_class.make_message()
                    if plugin_class.small_test > -1 :
                        img = num // plugin_class.skip 
                        if len(plugin_class.prompt_list) > 0:

                            p = plugin_class.prompt_list[img % len(plugin_class.prompt_list)]
                            m = p + ' - ' + m 
                        else:
                            m = ''
                    else:
                        img = 0

                    if plugin_class.image_series or plugin_class.make_corpus > 0:
                        img = ('00000000000' + str(plugin_class.step_count + plugin_class.corpus_offset))[- 10:]
                        print(img)
                    f = './pic/figure_' + str(img) + '.png'
                    
                    if plugin_class.make_corpus > 0:
                        f = './pic/' + str(img) + '.png'

                    if plugin_class.no_llm > 0 and plugin_class.step_count  > plugin_class.no_llm :
                        #print('exit before png save')
                        sys.exit()

                    #plugin_class.pygame_save(f)
                    plugin_class.image_save(f)

                    if int(img) > plugin_class.small_test and plugin_class.small_test > -1 :
                        sys.exit()

                    z = plugin_class.encode_image_to_base64(f)
                   
                    xx = ''
                    # open in the system browser!!
                    #subprocess.run(['open','data:image/png;base64,' + z])
                    #sys.exit()

                    print(m + '\n---')

                    if plugin_class.no_llm <= -1 or plugin_class.make_corpus > 0:
                        xx = model_class.do(image=z, context=None, text=m )
                    if plugin_class.no_llm > 0 and plugin_class.step_count > plugin_class.no_llm :
                        sys.exit()
                    elif plugin_class.no_llm > 0:
                        if pluginraw in pygamelist or pluginraw == '':
                            pygame.display.update()
                        #ticks = 15
                        #plugin_class.fps.tick(ticks)

                    print(xx)
                    xx = plugin_class.scrape(xx)

                    if plugin_class.make_corpus > 0:
                        a = plugin_class.action_string
                        model_class.write(scraped_output=a, raw_output=xx, raw_input=m, num_string=img)
                        paddle_message = ''

                    if len(plugin_class.message) > 0:
                        plugin_class.commands.append( str(plugin_class.step_count + 1) + ' ' + plugin_class.action_string + ' --' + str(plugin_class.message) + '--')
                    else:
                        plugin_class.commands.append(str(plugin_class.step_count + 1) + ' ' + plugin_class.action_string)
                    print('[' + str(plugin_class.step_count + 1) + ']', plugin_class.action_string)

                    #print('ball_vel', ball_vel, 'ball_pos', ball_pos)
                    
                    plugin_class.step_count += 1
                    plugin_class.message = ''
                    plugin_class.stats(True)

                    
                    if plugin_class.step_count >= plugin_class.small_test and plugin_class.small_test > -1 :
                        sys.exit()
                        pass

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


            if pluginraw in pygamelist or pluginraw == '':
                pygame.display.update()

            ticks = 60
            plugin_class.fps.tick(ticks)

    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')

    finally:
        print('---')
        plugin_class.stats(False)
        pass 
        


