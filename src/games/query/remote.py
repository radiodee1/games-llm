#!/usr/bin/env python3

import json
from default import Default


class Oai (Default):

    def __init__(self, model, streaming=False, chat=True, visual=True, key=None) -> None:
        super().__init__(model, streaming, chat, visual, key)
        self.url ='https://api.openai.com/v1/' 
        self.url_ending_chat = 'chat/completions'
        self.url_ending_generate = 'responses'
        self.openai_messages = []

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
        self.openai_messages += [{
            "role": 'user',
            "content": content, 
        }]

        self.data = {
            "model": self.model,
            "messages": self.openai_messages,
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
        content = [{
            'type':'text',
            'text': self.text 
        }]
        ##
        self.openai_messages += [{
            "role": 'user',
            "content": content, 
        }]

        self.data = {
            "model": self.model,
            "messages": self.openai_messages,
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
        """Overload this function"""
        return {}



