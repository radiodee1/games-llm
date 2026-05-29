from .default import DefaultPlugin, DefaultBare 
from .pygame_pong import PygamePongAgent
from .agent import LunarLanderAgent, PongAgent, BreakoutAgent
from .pygame_dots import PygameDotAgent
from .chat import ChatAgent

pluginlist = {
    'lunarlander'       : 'LunarLanderAgent',
    'pong'              : 'PongAgent',
    'pygamepong'        : 'PygamePongAgent',
    'pygame'            : 'PygamePongAgent',
    'breakout'          : 'BreakoutAgent',
    'dots'              : 'PygameDotAgent',
    'chat'              : 'ChatAgent'
}

pygamelist = [ 'pygamepong', 'pygame', 'dots' , 'chat']

