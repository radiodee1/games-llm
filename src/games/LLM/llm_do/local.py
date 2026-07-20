#!/usr/bin/env python3

from .default import DefaultLLM
from .remote import Oai

class Ollama (DefaultLLM):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        pass 

class OllamaImages (Oai): ## Oai

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url = 'http://localhost:11434/v1/'
        self.url_ending_chat = 'chat/completions'
        self.image_token_budget = None 
        
        pass 

    def payload(self, image=None, context=None, text=None):
        x = super().payload(image, context, text)
        if self.image_token_budget != None:
            self.data["options"] = { 
                "image_token_budget": self.image_token_budget
            }
            
        #print('images', len(self.images))
        print(self.data)
        return x

class Vjepa2Demo (DefaultLLM):
    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.write_to_text = False  ## skip json output
        pass 

    def do(self, image=None, context=None, text=None):
        from notebooks.vjepa2_demo_cpu import run_sample_inference 
        x = run_sample_inference()
        print('=====',x)
        return x 
