#!/usr/bin/env python3

from .default import DefaultLLM
from .remote import Oai
import os, json

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
        self.write_json_directory = 'workspace/VJEPA2_FILES/demo'
        pass 

    def do(self, image=None, context=None, text=None):
        from notebooks.vjepa2_demo_cpu import run_sample_inference 
        x = run_sample_inference()
        return x 

class Vjepa2Corpus (DefaultLLM):
    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.write_to_text = False  ## skip json output
        self.write_json_directory = 'workspace/VJEPA2_FILES/demo'
        pass 


    def write(self, scraped_output, raw_output , raw_input, num_string):
        PONG_CLASSES = json.load(open(os.path.join(os.path.expanduser('~'), self.write_json_directory, "json/classes_pong.json"), "r"))
        class_labels = [v for k,v in PONG_CLASSES.items() if k == scraped_output]
        print(class_labels)
        if len(class_labels) > 0:
            scraped_output = class_labels[0]
        else:
            scraped_output = 0
        print(scraped_output, class_labels, 'num <===')
        n = str('00000000' + str(num_string))[-5:]
        filename_string = './pic/video_image_label.json'
        pic_string = os.path.join( os.path.expanduser('~') , self.write_json_directory  ,'pic/train/output_' + n + '.mp4' )
        self.write_json[pic_string] = scraped_output 
        print('===',self.write_json,'===')
        with open(filename_string, 'w') as w:
            w.write(json.dumps(self.write_json) + '\n')


