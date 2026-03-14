

from .default import DefaultPlugin


class LunarLanderAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'LunarLander-v3'


class PongAgent( DefaultPlugin ):

    def __init__(self, mode="rgb_array") -> None:
        super().__init__(mode)
        self.agent = 'ALE/Pong-v5'
