#!/usr/bin/env python3

import json
from default import Default


class Ollama (Default):

    def __init__(self, model, streaming=False, chat=True, visual=True, key=None) -> None:
        super().__init__(model, streaming, chat, visual, key)
        pass 


