from .default import DefaultLLM
from .remote import Oai, Gem, Mis 
from .local import Ollama, OllamaImages

whitelist = {
    'qwen3-vl:2b'   : 'Ollama',
    'qwen3-vl:4b'   : 'Ollama',
    'gemma4:e4b'    : 'OllamaImages',
    'gpt-5.2'       : 'Oai',
    'gpt-4o'        : 'Oai',
    'gpt-5.4'       : 'Oai',
    'gemini-3-flash-preview' : 'Gem',
    'gemini-3-pro-preview'   : 'Gem',
    'gemini-2.5-flash'       : 'Gem',
    'mistral-large-2512'     : 'Mis',
    'pixtral-large-2411'     : 'Mis'
}
