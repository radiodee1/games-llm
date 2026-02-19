#!/usr/bin/env python3

import json
from .default import Default


class Oai (Default):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url ='https://api.openai.com/v1/' 
        self.url_ending_chat = 'chat/completions'
        self.url_ending_generate = 'responses'
        self.think = False

        pass 
    def payload_visual_chat(self):
        content = [{
            'type':'text',
            'text': self.text 
        },
        *[ 
            {
                'type': 'image_url',
                'image_url': {"url": f"data:image/png;base64,{q}", 'detail': 'high' } 
            } for q in self.images ]
          ##
        ]
        ##
        self.history += [{
            "role": 'user',
            "content": content, 
        }]

        self.data = {
            "model": self.model,
            "messages": self.history,
            "stream": self.streaming
        }
        pass 

    def payload_visual_generate(self):
        self.data = {
            "model": self.model,
            "input": self.text,
            "stream": self.streaming
        }
        pass 

    def payload_text_chat(self):
        content = [{
            'type':'text',
            'text': self.text 
        }]
        ##
        self.history += [{
            "role": 'user',
            "content": content, 
        }]

        self.data = {
            "model": self.model,
            "messages": self.history,
            "stream": self.streaming
        } 
 
        pass

    def payload_text_generate(self):
        self.data = {
            "model": self.model,
            "input": self.text,
            "stream": self.streaming
        }
        self.print(self.data)
        pass

    def payload_overload(self ):
        """Overload this function"""
        return {}

    def query_streaming_chat(self, x):
        for lines in x.iter_lines():
            if lines:
                if lines.startswith(b"data: "):
                    json_chunk = lines[6:]
                    if json_chunk == b"[DONE]" or not json_chunk:
                        break 
                    json_chunk = json_chunk.decode('utf-8')
                    #print(json_chunk)
                    chunk =  json.loads(json_chunk)['choices'][0]['delta']
                    #print(chunk)
                    self.r_temp += chunk.get('content', '')
                    continue


    def query_streaming_generate(self, x):
        for lines in x.iter_lines():
            if lines:
                chunk = json.loads(lines)
                self.print(chunk)
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
        #print(x)
        self.result = x['choices'][0]['message']['content']
        pass

    def query_generate(self, x):
        print(x)
        self.result = x['output'][0]['content'][0]['text']
        pass 

    def query_overload(self, x):
        """Overload this function"""
        return ''


class Gem (Oai):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url ='https://generativelanguage.googleapis.com/v1beta/openai/' 
        self.url_ending_chat = 'chat/completions'
        self.url_ending_generate = 'responses'
        self.think = False
        pass

