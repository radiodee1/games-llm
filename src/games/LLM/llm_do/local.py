#!/usr/bin/env python3

from .default import DefaultLLM
from .remote import Oai
import sys 

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

class Vjepa2MT (DefaultLLM):
    def __init__(self, model, streaming=False, chat=True, visual=True, think=False, key=None) -> None:
        super().__init__(model, streaming, chat, visual, think, key)
        self.write_to_text = False  ## skip json output
        self.write_json_directory = 'workspace/VJEPA2_FILES/demo'
        self.result = ''
        print('Vjepa2MT')
        pass 

    def do(self, image=None, context=None, text=None):
        x = self.pygame_mechanical()

        print(x , 'get_single_key here')
        return x 


    def pygame_mechanical(self):
        import pygame 
        pygame.init()
        screen = pygame.display.set_mode((320, 420))
        pygame.display.set_caption("Escape Key to quit.")
        try:
            image = pygame.image.load("./pic/figure_0.png")
        except pygame.error:
            image = pygame.Surface((320, 420))
            image.fill((200, 50, 50))

        screen.fill((255, 255, 255))  # White background
        screen.blit(image, (0, 0))  # Position x, y
        pygame.display.flip()

        waiting = True
        while waiting:
            event = pygame.event.wait()  # Pauses CPU until an event happens
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)

                if key_name == 'esc':
                    print('esc')
                if key_name == 'up':
                    return 'right.move.up'
                if key_name == 'down':
                    return 'right.move.down'
                if key_name == 'space':
                    return 'wait'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                print(key_name)
                waiting = False  # Exit loop on any key press
                return 'wait'


        pygame.quit()
        sys.exit()

