from .default import DefaultPlugin, DefaultBare 
from .pygame_pong import PygamePongAgent
from .agent import LunarLanderAgent, PongAgent, BreakoutAgent


pluginlist = {
    'lunarlander'       : 'LunarLanderAgent',
    'pong'              : 'PongAgent',
    'pygamepong'        : 'PygamePongAgent',
    'pygame'            : 'PygamePongAgent',
    'breakout'          : 'BreakoutAgent'
}

pygamelist = [ 'pygamepong', 'pygame' ]

