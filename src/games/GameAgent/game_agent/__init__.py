from .default import DefaultPlugin, DefaultBare 
from .pygame_pong import PygamePongAgent
from .agent import LunarLanderAgent, PongAgent, BreakoutAgent, PongVjepa2Agent
from .pygame_dots import PygameDotAgent
from .chat import ChatAgent

pluginlist = {
    'lunarlander'       : 'LunarLanderAgent',
    'pong'              : 'PongAgent',
    'pygamepong'        : 'PygamePongAgent',
    'pygame'            : 'PygamePongAgent',
    'breakout'          : 'BreakoutAgent',
    'dots'              : 'PygameDotAgent',
    'chat'              : 'ChatAgent',
    'ssv'               : 'PongVjepa2Agent'
}

pygamelist = [ 'pygamepong', 'pygame', 'dots' , 'chat']

