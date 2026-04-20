#!/usr/bin/env python3

import json
from .default import DefaultLLM
from .remote import Oai

class Ollama (DefaultLLM):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        pass 

class OllamaImages (Oai):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.url = 'http://localhost:11434/v1/'
        self.url_ending_chat = 'chat/completions'
        pass 




