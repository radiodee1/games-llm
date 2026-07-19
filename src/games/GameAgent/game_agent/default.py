#!/usr/bin/env python3

import gymnasium as gym
import ale_py
import sys 
import pygame
import cv2
import base64
import time
import shutil
import math
import ffmpeg 
import glob
import os 

class DefaultBare:

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None
        self.truncated = False
        self.terminated = False

        self.smaller = inverse_size 
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
        self.start_time = 0
        self.end_time = 0

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
        self.action_meaning = [] # combined meaning information
        self.meaning = [] # just the human readable meaning
        self.action_string = ''
        self.frame_skip = 1
        self.repeat_action_probability = 0.0 
        self.total = -1 

        self.prompt_string = ''
        self.fps = None
        self.show_image = show_image

        self.l_score = 0
        self.r_score = 0
        self.model = ''
        self.step_count = 0
        self.serves_num = 0
        pass 

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    def prune_png(self, num=3):
        ## get latest figure
        ii = 'pic/figure_0.png'
        img = ('00000000000' + str(0))[- 10:]
        #print(num, 'num')
        ## find latest number
        g = glob.glob('pic/figure_x*.png')
        g.sort()
        #print(g)
        if len(g) > 0:
            i = g[-1]
            n = i[len('pic/figure_x'): - len('.png')]
            #print(i, n)
            j = int(n)
            #print('int', j)
            j = j + 1 
            img = ('00000000000' + str(j))[- 10:]

        ## put file in queue 
        os.rename(ii, 'pic/figure_x' + str(img) + ".png")   
        ## get whole queue
        g = glob.glob('pic/figure_x*.png')
        g.sort()
        z = 0 
        ## trim beginning of queue
        while len(g) > num and z < 100:
            os.remove(g[0])

            g = glob.glob('pic/figure_x*.png')
            g.sort() 
            z += 1
        #print(len(g), 'g len', g)
        ## move all of queue to low position 
        g = glob.glob('pic/figure_x*.png')
        g.sort()
        j = 0
        
        for i in range(len(g)):
            n = g[i][len('pic/figure_x'): - len('.png')]
            #print(i, n)
            j = int(n)
            if j != i:
                img_i = ('00000000000' + str(i))[- 10:]
                img_j = ('00000000000' + str(j))[- 10:]
                os.rename('pic/figure_x' + str(img_j) + '.png', 'pic/figure_x' + str(img_i) + '.png')
        #g = glob.glob('pic/figure_x*.png')
        #g.sort() 
        #print(len(g), 'final g len', g)
        return

    def convert_video(self, num=0):
        try:
            (
                ffmpeg
                .input("pic/figure_x%010d.png")
                #.option("y") # Overwrite output file if it exists
                .filter('fps', fps=16, round='up')
                .filter('scale', w=648, h=448, flags='neighbor')
                .output(
                    "pic/output_" + str(num) + ".mp4",
                    pix_fmt='yuv444p',
                    vcodec="libx264", # Video codec
                    preset="medium"
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            print("Processing video...", 'pic/figure_%010d.png')
            print("Done!")
        except ffmpeg.Error as e:
            print("ffmpeg error:",  e.stderr.decode())

        return 

    def pygame_save(self, f):
        pass

    def image_save(self, filename):
        self.pygame_save(filename)
        pass

    def make_message(self) -> str:
        self.read_actions()
        #print(self.action_meaning, 'meaning')
        m = [ str( '"' + i['meaning'] + '"') for i in self.action_meaning ]
        #print(m, 'm')
        txt = self.prompt_string + ' ' 
        if len(self.action_meaning) > 0:
            txt += 'These are the actions you can take: ' + ', '.join(m)
        return str(txt)

    def read_actions(self):
        if isinstance(self.env.action_space, gym.spaces.Discrete):
            
            x = self.env.unwrapped.get_action_meanings()
            #print(x, 'x')
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
            #print(self.action_meaning, 'read_actions')

    def no_description(self):
        pass 

    def stats(self, short=True):
        if not short:
            self.print_in_columns(self.commands)
        print()
        print("model:", self.model)
        if self.serves_num > 0:
            print("serves_num:", self.serves_num)
          
        print("l_score:", self.l_score, "r_score:", self.r_score)
        single = 0 
        if not short:
            single = 0 
        print("step-count:", (self.step_count + single))
        self.end_time = time.perf_counter()

        elapsed_min = (self.end_time - self.start_time) // 60 
        elapsed_sec = (self.end_time - self.start_time) - elapsed_min * 60
        elapsed_sec = '0000' + str(int(elapsed_sec))
        elapsed_sec = elapsed_sec[-2:]
        elapsed_hrs = elapsed_min // 60
        if elapsed_hrs > 0:
            elapsed_min = elapsed_min - elapsed_hrs * 60 
            elapsed_min = '0000' + str(int(elapsed_min))
            elapsed_min = elapsed_min[-2:]
            print(f"Elapsed time: {elapsed_hrs}:{elapsed_min}:{elapsed_sec} hrs:min:sec")
        else:
            print(f"Elapsed time: {elapsed_min:.0f}:{elapsed_sec} minutes")
        print('---')
        if short:
            return
        return 

    def draw(self, canvas=None):
        pass 

    def init(self):
        self.start_time = time.perf_counter()
        pass 

    def reset(self):
        pass 

    def scrape(self, txt, replace=False):
        ## make list of high rfind() ##
        x = []
        n = []
        s = [] 
        for i in range(len(self.action_meaning)):
            xx = self.action_meaning[i]['meaning']
            discrete = self.action_meaning[i]['num']
            x.append(txt.rfind(xx))
            n.append(discrete)
            s.append(xx)
        #print(x, n, s)

        ## find highest ##
        h = -1 
        index = -1 
        for i in range(len(n)):
            if x[i] > -1 and x[i] > h: # old:
                h = x[i]
                index = i 
        if index > -1:
            #print(n[index])
            self.action = int(n[index])
        else:
            self.action = 0 

        if replace and h > -1:
            txt = txt[:h] + s[index] + txt[h + len(s[index]):]
            
        self.action_string = s[index]
        return txt

    def print_in_columns(self, data):
        if not data:
            return
        data = [str(item) for item in data]
        try:
            terminal_width = shutil.get_terminal_size().columns
        except OSError:
            terminal_width = 80
        max_len = max(len(item) for item in data)
        num_items = len(data)
        column_width = max_len + 2
        num_cols = terminal_width // column_width
        if num_cols == 0:
            num_cols = 1
            column_width = terminal_width
        num_rows = math.ceil(num_items / num_cols)
        for row in range(num_rows):
            for col in range(num_cols):
                index = col * num_rows + row
                if index < num_items:
                    d = str(data[index]) + '          '
                    d = d[: column_width]
                    print(d, end="")
            print() # Newline at the end of each row


class DefaultPlugin (DefaultBare):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.agent = ""
        self.render_mode = mode 
        self.env = None
        self.action = None
        self.truncated = False
        self.terminated = False
        self.reward = 0 
        self.show_image = show_image
        pass 

    def draw(self, surface=None):
        if surface != None:
            sys.exit()
        #print('----', self.action, '----')
        observation, reward, terminated, truncated, info = self.env.step(int(self.action))
        self.reward = reward
        if terminated:
            self.terminated = terminated
        if truncated:
            self.truncated = truncated
        #self.r_score += reward
        #print(observation)
        #print(info)
        pass 

    def init(self):
        super().init()
        if self.frame_skip != None and self.frame_skip >= 0:
            self.env = gym.make(self.agent, render_mode=self.render_mode, frameskip=int(self.frame_skip), repeat_action_probability=self.repeat_action_probability)
            print('skip', self.frame_skip)
        else:
            self.env = gym.make(self.agent, render_mode=self.render_mode)
        pass 

    def reset(self):
        self.truncated = False
        self.terminated = False
        observation, info = self.env.reset()
        self.start_sequence()
        cv2.destroyAllWindows()
        pass 

    def start_sequence(self):
        pass 

    def image_save(self, filename):
        self.pygame_save(filename)
        pass 

    def pygame_save(self, f):
        if self.render_mode != 'rgb_array':
            return
        r = self.env.render()
        surface = pygame.surfarray.make_surface(r)
        if True:
            surface = pygame.transform.rotate(surface, 270)
            surface = pygame.transform.flip(surface, True, False)
        surface = pygame.transform.scale_by(surface, 4 // self.smaller )
        pygame.image.save(surface, f)

        if self.show_image:
            #print(f, 'cv2')
            frame_bgr = cv2.cvtColor(r, cv2.COLOR_RGB2BGR)
            cv2.namedWindow('Games', cv2.WINDOW_GUI_NORMAL)
            cv2.imshow('Games', frame_bgr)
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


