from .default import DefaultBare


class ChatAgent ( DefaultBare ):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.agent = 'Chat'
        self.prompt_string = ""
        self.action_meaning = []
        self.prompt_list = [ 'Say something inspirational about how to use your time wisely.' ]

    def make_message(self) -> str:
        return self.prompt_string

    def scrape(self, txt, replace=False):
        return txt

    def stats(self, short=True):
        if not short:
            print('-+', self.prompt_string, '+-')
            with open('./pic/llm.' + self.agent + '.txt', 'w') as x:
                x.write(self.agent + ' : '  + ' '.join( self.prompt_string.strip().strip('--').strip().split('\n'))  )
                x.close()


        
