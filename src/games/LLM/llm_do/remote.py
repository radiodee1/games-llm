#!/usr/bin/env python3

import json
from .default import DefaultLLM 


class Oai (DefaultLLM):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url ='https://api.openai.com/v1/' 
        self.url_ending_chat = 'chat/completions'
        self.url_ending_generate = 'responses'
        self.image_type_label = 'image_url'
        self.api_key_name = "OPENAI_API_KEY"
        #self.think = False

        pass 

    def payload_visual_chat(self):
        self.payload_previous_chat()

        content = [{
            'type':'text',
            'text': self.text 
        },
        *[ 
            {
                'type': self.image_type_label,
                self.image_type_label: {"url": f"data:image/png;base64,{q}", 'detail': 'high' } 
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
            "stream": self.streaming,
            #"reasoning_effort": "none",
            #"temperature": 0.1
        }
        #print(self.data)
        pass 

    def payload_visual_generate(self):
        self.data = {
            "model": self.model,
            "input": self.text,
            "stream": self.streaming
        }
        pass 

    def payload_text_chat(self):
        self.payload_previous_chat()

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

    def payload_previous_chat(self):
        if len(self.result) > 0:
            content = [{
                'type':'text',
                'text': self.result
            }]
            ##
            self.history += [{
                "role": 'assistant',
                "content": content, 
            }]
        pass 

    def payload_text_generate(self):
        self.data = {
            "model": self.model,
            "input": self.text,
            "stream": self.streaming
        }
        self.print(self.data)
        pass

    def payload_think(self):
        #self.data['reasoning_effort'] = 'high'
        self.print(self.data)

    def payload_overload(self ):
        """Overload this function"""
        return {}

    def query_streaming_chat(self, x):
        for lines in x.iter_lines():
            if lines:
                #print(lines)
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
        self.print(x)
        self.result = x['choices'][0]['message']['content']
        #print('===', self.result, '===')
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
        self.api_key_name = "GEMINI_API_KEY"
        pass


class Mis (Oai):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url ='https://api.mistral.ai/v1/' 
        self.url_ending_chat = 'chat/completions'
        self.url_ending_generate = 'responses'
        self.think = False
        self.api_key_name = "MISTRAL_API_KEY"
        pass

class Anth (Oai):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url ='https://api.anthropic.com/v1/' 
        self.url_ending_chat = 'messages'
        self.url_ending_generate = 'completions'
        self.header_anthropic_version = '2023-06-01'
        self.max_tokens = 1024
        self.image_type_label = 'image'
        self.chat = True ## <-- only chat option 
        self.think = False
        self.api_key_name = "ANTHROPIC_API_KEY"
        pass

    def make_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": str( self.api_key ),
            "anthropic-version": self.header_anthropic_version
        }

    def payload(self, image=None, context=None, text=None):
        x = super().payload(image, context, text)
        self.data['max_tokens'] = self.max_tokens 
        return x  

    def query_chat(self, x):
        self.result = str(x['content'][0])

    def payload_visual_chat(self):
        self.payload_previous_chat()

        content = [{
            'type':'text',
            'text': self.text 
        },
        *[ 
            {
                'type': self.image_type_label,
                   'source': {'type': 'base64', 'media_type': 'image/png'  ,"data": f"{q}" } 
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
            "stream": self.streaming,
            #"reasoning_effort": "none",
            #"temperature": 0.1
        }
        #print(self.data)
        pass 

    def query_streaming_chat(self, x):
        for lines in x.iter_lines():
            if lines:
                #print(lines)
                if lines.startswith(b"data: "):
                    decoded_line = lines.decode('utf-8')
                    if decoded_line.startswith("data: "):

                        json_str = decoded_line[6:]
                        event_data = json.loads(json_str)
                    
                        # Check for the 'content_block_delta' event type for actual text
                        if event_data.get("type") == "content_block_delta":
                            text = event_data["delta"].get("text", "")
                            #print(text, end="", flush=True)
                            self.r_temp += str(text)


