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
        self.write_json_directory = 'workspace/VJEPA2_FILES/demo'
        pass 

    def do(self, image=None, context=None, text=None):
        from notebooks.vjepa2_demo_cpu import run_sample_inference
        x = run_sample_inference(True)
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
        x = self.evdev_get_key()

        print(x , 'get_single_key here')
        return x 

    def get_single_key(self):
        from pynput import keyboard
        self.result = None

        '''
        import keyboard
        import time

        print("Press 'q' to exit the loop...")

        while True:
            # Check if a specific key is pressed
            if keyboard.is_pressed('q'):
                print("You pressed 'q'. Exiting...")
                break
                
            # Read and print any key as it is pressed
            key = keyboard.read_key()
            print(f"Key pressed: {key}")
            
            time.sleep(0.1)  # Small delay to prevent high CPU usage

        
        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.esc:
                    self.result = 'wait'
                    break
                else:
                    print('Received event {}'.format(event))

        '''
        # Start the listener and block until a target key is pressed
        with keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except Exception as e:
                print('{0} was pressed'.format(e.args[0]))
                
        print(self.result, '<<<<')
        return self.result

    def on_press(self, key):
        #from pynput import keyboard
        if key == keyboard.Key.up:
            self.result = "UP_PRESSED"
            return False
        elif key == keyboard.Key.down:
            self.result = "DOWN_PRESSED"
            return False
        elif key == keyboard.Key.space:
            self.result = "SPACE_PRESSED"
            return False
        elif key == keyboard.Key.esc:
            self.result = "ESC_PRESSED"
            return False

    def evdev_get_key(self):
        import evdev
        from evdev import InputDevice, categorize, ecodes

        # Find your keyboard device (e.g., /dev/input/event0)
        # You can list devices using: python3 -c "import evdev; print([evdev.InputDevice(fn) for fn in evdev.list_devices()])"
        devices = [InputDevice(fn) for fn in evdev.list_devices()]
        keyboard = None

        for dev in devices:
            if 'keyboard' in dev.name.lower() or 'kbd' in dev.name.lower():
                keyboard = dev
                break

        if not keyboard:
            # Fallback to a specific path if auto-detect fails
            keyboard = InputDevice('/dev/input/event0')

        print(f"Listening on {keyboard.path} ({keyboard.name})")

        # Loop through events
        for event in keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                print('data', data)
                if data.keystate == data.key_down:
                    print(f"Key pressed: {data.keycode}")
                    self.result = data.keycode
                    return

