from .default import DefaultLLM
from .remote import Oai, Gem, Mis, Anth 
from .local import Ollama, OllamaImages, Vjepa2Demo, Vjepa2Corpus

whitelist = {
    'qwen3-vl:2b'   : 'Ollama',
    'qwen3-vl:4b'   : 'OllamaImages',
    'qwen3-vl:8b'   : 'Ollama',
    'gemma4:e4b'    : 'OllamaImages',
    'gpt-5.2'       : 'Oai',
    'gpt-4o'        : 'Oai',
    'gpt-4o-mini'   : 'Oai',
    'gpt-5.4'       : 'Oai',
    'gemini-3-flash-preview' : 'Gem',
    'gemini-2.5-flash'       : 'Gem',
    'mistral-large-2512'     : 'Mis',
    'pixtral-large-2411'     : 'Mis',
    'claude-3-5-sonnet-20240620'    : 'Anth',
    'vjepa':       'Vjepa2Demo',
    'vjepacorpus':  'Vjepa2Corpus'
}

def whitelist_helper(model):
    if len(model.split(':')) > 1:
        return 'OllamaImages'
    m = model[0:4]
    for i in whitelist:
        #print(i, 'model')
        if i.startswith(m):
            return whitelist[i]


