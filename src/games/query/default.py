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

    def __init__(self, model, streaming=False, chat=True, visual=True) -> None:
        self.images = []
        self.context = []
        self.text = ''
        self.result = ''
        self.last_code = 0
        self.model = model 
        self.headers = {}
        self.data = {} ## put payload here.
        self.history = []

        self.visual = visual ## visual or not visual
        self.streaming = streaming ## streaming or not streaming
        self.chat = chat ## chat or generate
        self.think = True ## think or not think
        self.url = 'http://localhost:11434/api/'

        pass

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def image_to_string(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
        

    def payload(self, image=None, context=None, text=None):
        if image is not None and isinstance(image, str):
            self.images.append(image)
        if context is not None and isinstance(context, list):
            self.context = context
        if text is not None and isinstance(text, str):
            self.text = text

        if self.chat:
            if self.visual:
                self.payload_visual_chat()
            else:
                self.payload_text_chat()
        else:
            if self.visual:
                self.payload_visual_generate()
            else:
                self.payload_text_generate()

        p = self.payload_overload()
        if len(p) > 0:
            self.data = p 


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

