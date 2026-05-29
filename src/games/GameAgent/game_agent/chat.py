from .default import DefaultBare


class ChatAgent ( DefaultBare ):

    def __init__(self, mode="rgb_array", inverse_size=4, show_image=True) -> None:
        super().__init__(mode, inverse_size, show_image)
        self.agent = 'Chat'
        self.prompt_string = ""
        self.action_meaning = []

    def make_message(self) -> str:
        return self.prompt_string

    def scrape(self, txt, replace=False):
        return txt
