'''Configuration of the routes, or vocabulary of the bot'''
from bottery.conf.patterns import Pattern, DefaultPattern, \
    HookableFuncPattern, HookPattern
from bottery.views import pong, access_api_rules
from views import help_text, say_help, END_HOOK_LIST, two_tokens


rules = {'tec': {'rank': 'http://brasilico.pythonanywhere.com/_rank?words=',
                 'filtra':
                  'http://brasilico.pythonanywhere.com/_filter_documents?afilter=',
                 'capitulo':
                  'http://brasilico.pythonanywhere.com/_document_content/',
                 '_message': 'Informe o comando: '
                }
        }

 
rules_cep = {'cep': {'busca': 'http://api.postmon.com.br/v1/cep/',
                     '_message': 'Informe o comando: '
                }
        }


conversation = HookPattern(END_HOOK_LIST)
patterns = [
    conversation,
    Pattern('ping', pong),
    Pattern('help', help_text),
    HookableFuncPattern('tec', access_api_rules, two_tokens, conversation, rules=rules),
    HookableFuncPattern('cep', access_api_rules, two_tokens, conversation, rules=rules_cep),
    DefaultPattern(say_help)
]
 