#!/usr/bin/env python3

import json
import requests
import os 
import time
import base64
import argparse 

from dotenv import load_dotenv

load_dotenv()

class Default:

    def __init__(self, model, streaming=False, chat=True, visual=True, key=None) -> None:
        self.images = []
        self.context = []
        self.text = ''
        self.result = ''
        self.raw_result = None
        self.last_code = 0
        self.model = model 
        self.headers = {}
        self.data = {} ## put payload here.
        self.history = []
        self.time_start = -1
        self.time_end = -1

        self.context_size = 1 
        self.images_size = 3 
        self.history_size = 1 

        self.visual = visual ## visual or not visual
        self.streaming = streaming ## streaming or not streaming
        self.chat = chat ## chat or generate
        self.think = True ## think or not think
        self.url = 'http://localhost:11434/api/'
        self.api_key = key 

        self.r_temp = ''
        self.think_temp = ''

        print('Default')
        pass

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def image_to_string(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
        
    def start_time(self):
        self.time_start = time.perf_counter()

    def end_time(self):
        self.time_end = time.perf_counter()
        #end_time = time.perf_counter()
        elapsed_min = (self.time_end - self.time_start) // 60 
        elapsed_sec = (self.time_end - self.time_start) - elapsed_min * 60
        elapsed_sec = '0000' + str(int(elapsed_sec))
        elapsed_sec = elapsed_sec[-2:]
        print(f"Elapsed time: {elapsed_min:.0f}:{elapsed_sec} minutes")


    def make_headers(self):
        if self.api_key is not None:
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": str("Bearer " + self.api_key ) 
            }

    def payload(self, image=None, context=None, text=None):
        if image is not None and isinstance(image, str):
            self.images.append(image)
        if image is not None and isinstance(image, list):
            self.images += image
        if context is not None and isinstance(context, list):
            self.context = context
        if text is not None and isinstance(text, str):
            self.text = text
        
        self.start_time()
        
        if self.chat:
            self.url += 'chat'
            if self.visual:
                self.payload_visual_chat()
            else:
                self.payload_text_chat()
        else:
            self.url += 'generate'
            if self.visual:
                self.payload_visual_generate()
            else:
                self.payload_text_generate()

        p = self.payload_overload()
        if len(p) > 0:
            self.data = p 
        self.make_headers()
        ## done ##

    def payload_visual_chat(self):
        self.history += [{
            "role": "system",
            "content": self.text,
            "images" : self.images
        }]

        self.data  = {
            "model": self.model,
            "messages": self.history,
            "stream": self.streaming
        }
        pass 

    def payload_visual_generate(self):
        self.data = {
            "model": self.model,
            "prompt": self.text,
            "images": self.images,
            "context": self.context,
            "stream": self.streaming
        }
        pass 

    def payload_text_chat(self):
        self.history += [{
            "role": "system",
            "content": self.text,
        }]

        self.data  = {
            "model": self.model,
            "messages": self.history,
            "stream": self.streaming
        }
 
        pass

    def payload_text_generate(self):
        self.data = {
            "model": self.model,
            "prompt": self.text,
            "context": self.context,
            "stream": self.streaming
        }
        pass

    def payload_overload(self):
        return {}

    def query(self):
        self.think_temp = ''
        self.r_temp = ''
        if self.streaming:
            with requests.post(self.url, json=self.data, stream=self.streaming) as x:
                x.raise_for_status()
                if self.chat:
                    self.query_streaming_chat(x)
                else:
                    self.query_streaming_generate(x)
                self.result = self.think_temp + '\n---\n' + self.r_temp + '\n---'
            pass
        else:
            self.raw_result = requests.post(self.url, json=self.data, stream=self.streaming)
            #self.raw_result = self.raw_result.json() ## <-- use me??
            if self.chat:
                self.query_chat()
            else:
                self.query_generate()
            pass
        self.end_time()
        pass 
        
    def query_streaming_chat(self, x):
        for lines in x.iter_lines():
            if lines:
                chunk = json.loads(lines)
                
                chunk_message = chunk.get('message', {})
                self.r_temp += chunk_message.get('content', '')
                self.think_temp += chunk_message.get('thinking', '')
                print(chunk)
                self.r_temp += chunk.get('response', '')
                self.think_temp += chunk.get('thinking','')
                
                if chunk.get('done'):
                    #sys.exit()
                    break
        pass 

    def query_streaming_generate(self, x):
        for lines in x.iter_lines():
            if lines:
                chunk = json.loads(lines)
                if 'context' in chunk:
                    self.context = chunk['context']
                print(chunk)
                self.r_temp += chunk.get('response', '')
                self.think_temp += chunk.get('thinking','')
                
                if chunk.get('done'):
                    #sys.exit()
                    break

        pass

    def query_chat(self):
        x = self.raw_result
        xx = ''
        print('x', x)
        if 'message' in x and 'content' in x['message']:
            xx = x['message']['content']
            ## xx = scrape(xx)

            self.history += [{
                'role': 'assistant',
                'content': xx 
            }]
            '''
            if len(message) > 0:
                commands.append(xx + ' --' + str(message) + '--')
            else:
                commands.append(xx)
            '''
            print(xx, history)
        else:
            xx = ''

        if 'done' in x and x['done'] == False:
            print('not done!!')
            print(x)
        self.result = xx 
        pass

    def query_generate(self):
        x = self.raw_result
        xx = ''
        if 'done' in x and x['done'] == False:
            message = ''
            ## pygame.display.set_caption('Partial ' + str(num // skip + 1))   
            #continue  ## skip next part
            if 'response' in x and len(x['response']) > 0:
                print(x['response'])
            x['response'] = ''
            xx = ''
        
        elif 'response' in x:
            xx = x['response']
            ## xx = scrape(xx)
            #er = 0 
        else:
            xx = ''
        #####
        if 'context' in x:
            self.context = str(x['context'])
        else:
            pass 
            #cc = '' # keep the context from last pass 
            print(x)
            #sys.exit()
        self.result = xx 
        pass 

    def trim(self):
        if self.images_size > -1 and self.images_size < len(self.images):
            self.images = self.images[ - self.images_size : ]
            print('len images', len(self.images))
        if self.context_size > -1 and self.context_size < len(self.context):
            self.context = self.context[ - self.context_size : ]
            print('len context', len(self.context))
        if self.history_size > -1 and self.history_size < len(self.history):
            self.history = self.history[ - self.history_size : ]
            print('len history', len(self.history))

    def do(self, image=None, context=None, text=None):
        self.payload(image=image, context=context, text=text)
        self.query()
        self.trim()
        return self.result

