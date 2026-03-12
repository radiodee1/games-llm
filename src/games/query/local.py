#!/usr/bin/env python3

import json
from .default import DefaultLLM


class Ollama (DefaultLLM):

    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        pass 


