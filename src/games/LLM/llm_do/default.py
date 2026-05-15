#!/usr/bin/env python3

import json
import requests
import os 
import time
import base64

#from dotenv import load_dotenv

#load_dotenv()

class DefaultLLM:

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
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
        self.show_payload = False

        self.context_size = -1 
        self.images_size = 3 
        self.history_size = -1 

        self.visual = visual ## visual or not visual
        self.streaming = streaming ## streaming or not streaming
        self.chat = chat ## chat or generate
        self.think = think ## think or not think
        self.url_derived = ''
        self.url = 'http://localhost:11434/api/'
        self.url_ending_chat = 'chat'
        self.url_ending_generate = 'generate'
        self.api_key = key 

        self.r_temp = ''
        self.think_temp = ''
        self.print_to_screen = False
        self.write_to_text = False
        self.skip_errors = False
        self.write_only = False
        self.write_message = ""
        self.temperature = -1 
        self.top_p = -1 
        self.reasoning_effort = None ## 'none', 'low', 'medium', 'high'
        self.print('Default', model)
        pass

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def print(self, *args):
        if self.print_to_screen:
            print(*args)

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
        self.print(f"Elapsed Post Time: {elapsed_min:.0f}:{elapsed_sec} minutes")

    def process_context(self, cc):
        if cc.startswith('['):
            cc = cc[1:]
        if cc.endswith(']'):
            cc = cc[:-1] # rm first and last char
        ctx = cc.split(',')
        ctx = [ int(x) for x in ctx ]
        return ctx 

    def make_headers(self):
        if self.api_key is not None:
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": str("Bearer " + self.api_key ) 
            }

    def payload(self, image=None, context=None, text=None):
        if image is not None and isinstance(image, str):
            self.images.append(image)
        if context is not None and isinstance(context, list) and not self.chat:
            self.context = context
        else:
            ## do nothing. context is filled in previous 'self.query'
            pass 
        if not self.chat:
            if isinstance(self.context, str):
                self.context = self.process_context(self.context)
            if context is not None and isinstance(context, str):
                self.context = self.process_context(context)

        if text is not None and isinstance(text, str):
            self.text = text
        
        self.start_time()
        self.trim_dict()

        if self.chat:
            self.url_derived = self.url + self.url_ending_chat
            if self.visual:
                self.payload_visual_chat()
            else:
                self.payload_text_chat()
        else:
            self.url_derived = self.url + self.url_ending_generate
            if self.visual:
                self.payload_visual_generate()
            else:
                self.payload_text_generate()

        p = self.payload_overload()
        if len(p) > 0:
            self.data = p

        if self.think:
            self.payload_think()

        if self.temperature > -1:
            self.payload_temperature()
        
        if self.top_p > -1:
            self.payload_top_p()

        self.make_headers()
        if self.show_payload:
            print(self.data)

        ## done ##

    def payload_think(self):
        self.data['think'] = True

    def payload_temperature(self):
        if str(type(self).__name__) == 'Oai' and self.reasoning_effort != None:
            self.data['reasoning_effort'] = self.reasoning_effort
        self.data['temperature'] = self.temperature 

    def payload_top_p(self):
        self.data['top_p'] = self.top_p 

    def payload_visual_chat(self):
        self.payload_previous_chat() 
        
        print('images', len(self.images))
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
        self.payload_previous_chat() 

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

    def payload_previous_chat(self):
        if len(self.result) > 0:
            self.history += [{
                "role": 'assistant',
                "content": self.result, 
            }]
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
        """Overload this function"""
        return {}

    def query(self):
        if self.write_only:
            return
        self.think_temp = ''
        self.r_temp = ''
        #print(self.data)
        if self.streaming:
            with requests.post(self.url_derived, json=self.data, stream=self.streaming, headers=self.headers) as x:
                if not self.skip_errors:
                    x.raise_for_status()
                if self.chat:
                    self.query_streaming_chat(x)
                else:
                    self.query_streaming_generate(x)
                self.result = self.think_temp + '\n---\n' + self.r_temp + '\n---'
            #print('===',self.result,'===')
            pass
        else:
            self.raw_result = requests.post(self.url_derived, json=self.data, stream=self.streaming, headers=self.headers)
            self.raw_result = self.raw_result.json() 
            if self.chat:
                self.query_chat(self.raw_result)
            else:
                self.query_generate(self.raw_result)

            q = self.query_overload(self.raw_result)
            if len(q.strip()) > 0:
                self.result = q
        self.end_time()
        pass 
        
    def query_streaming_chat(self, x):
        for lines in x.iter_lines():
            if lines:
                chunk = json.loads(lines)
                
                chunk_message = chunk.get('message', {})
                self.r_temp += chunk_message.get('content', '')
                self.think_temp += chunk_message.get('thinking', '')
                self.print(chunk)
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
                self.print(chunk)
                self.r_temp += chunk.get('response', '')
                self.think_temp += chunk.get('thinking','')
                
                if chunk.get('done'):
                    #sys.exit()
                    break

        pass

    def query_chat(self, x):
        xx = ''
        if 'message' in x and 'content' in x['message']:
            xx = x['message']['content']

            self.history += [{
                'role': 'assistant',
                'content': xx 
            }]
            self.print(xx, self.history)
        else:
            xx = ''

        if 'done' in x and x['done'] == False:
            self.print('not done!!')
            self.print(x)
        self.result = xx 
        pass

    def query_generate(self, x):
        xx = ''
        if 'done' in x and x['done'] == False:
            if 'response' in x and len(x['response']) > 0:
                self.print(x['response'])
            x['response'] = ''
            xx = ''
        
        elif 'response' in x:
            xx = x['response']
        else:
            xx = ''
        #####
        if 'context' in x:
            self.context = str(x['context'])
        else:
            pass 
            self.print(x)
        self.result = xx 
        pass 

    def query_overload(self, x):
        """Overload this function"""
        return ''

    ## call inside payload ##
    def trim_dict(self): 
        if self.images_size > -1 and self.images_size < len(self.images):
            self.images = self.images[ - self.images_size : ]
            if self.images_size == 0:
                self.images = [] 
            self.print('len images', len(self.images), self.images_size)
        if self.context and self.context_size > -1 and self.context_size < len(self.context):
            self.context = self.context[ - self.context_size : ]
            if self.context_size == 0:
                self.context = [] 
            self.print('len context', len(self.context), self.context_size)
        if self.history_size > -1 and self.history_size < len(self.history):
            self.history = self.history[ - self.history_size : ]
            if self.history_size == 0:
                self.history = [] 
            self.print('len history', len(self.history), self.history_size)

    def do(self, image=None, context=None, text=None):
        self.payload(image=image, context=context, text=text)
        #self.print(self.data)
        self.query()
        return self.result

    def write(self, scraped_output, raw_output , raw_input, num_string):
        self.print('some data', 'scraped_output', scraped_output,'raw_output', raw_output,'raw_input', raw_input,'num_string', num_string)
        #image_string = './pic/' + str(num_string) + '.png'
        image_string =   str(num_string) + '.png'
        if not self.write_to_text:
            return
        filename_string = './pic/' + str(num_string) + '.json'
        f = {
            "id": num_string,
            "image": image_string,
            "conversations": [
                {
                    'from': 'human',
                    'value': '<image>\n' + raw_input
                    
                },
                {
                    'from': 'gpt',
                    'value': raw_output + "\n" + scraped_output
                }
            ]
        }
        with open(filename_string, 'w') as w:
            w.write(json.dumps(f) + '\n')

        return
