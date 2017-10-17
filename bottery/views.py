import json
import shlex
import sys
from urllib.request import urlopen


def pong(message):
    return 'pong'


def locate_next(words, rules, level=1):
    '''Recursively process the rule chain
    Used by view access_api_rules'''
    try:
        # alist = words.split(' ')
        # (like in shell, preserves expressions in quotes)
        alist = shlex.split(words)
        next_level = {}
        url = ""
        for key, value in rules.items():
            if key == alist[0]:
                # print('key found =', alist[0])
                if isinstance(value, dict):
                    for k, v in value.items():
                        next_level[k] = v
                else:
                    url = value

        if url:
            return url, level
        else:
            if len(alist) > 1:
                return locate_next(' '.join(alist[1:]),
                                   next_level, level+1)
            return next_level, level
    except AttributeError:
        print("Atribute error. Possibly misconfiguration of rules:",
              sys.exc_info()[0])
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def process_parameters(name, level, params):
    '''Process the parameter chain
    Used by view access_api_rules'''
    key = name.strip() + ':' + str(level)
    param_list = params.get(key, None)
    if param_list is None:
        return None
    result = []
    n_required = 0
    for param in param_list:
        result.append(param['name'])
        if param['required'] is True:
            n_required += 1

    return result, n_required


def access_api_rules(message, rules, params_dict=None):
    '''Acess a JSON 'REST' API maped by rules
    text: a phrase, a sequence of words by space passed by the Pattern object
    rules: a dict on format rules = {'command1': {'subcommand1': 'url1',
                                                 {'subcommand2': 'url2'} },
                                     'command2': 'url3'
                                    }
    params_dict: a dict/list on format
    params = {'command:level': [{'name': 'name1', 'required': True},
                                {'name': 'name2', 'required': False}
                               ],
              'command2:level': [{'name': 'name2.1', 'required': True}]
             }
    '''
    text = message.text
    # Splits like in shell: splits/tokenizes on spaces,
    # preserving expressions between quotes
    alist = shlex.split(text)
    url, level = locate_next(text, rules)
    if isinstance(url, dict):
        if url == {}:
            return 'Unrecognized command, exiting...', False
        message = url.pop('_message', '')
        return message + ' - '.join([key for key in url]), True
    str_params = ''
    if params_dict is None:
        str_params = '%20'.join(alist[level:])
        if not str_params:
            return 'Enter parameters: ', True
    else:
        n_params_passed = len(alist) - level
        params_list, n_required = process_parameters(alist[level-1],
                                                     level, params_dict)
        if n_params_passed < n_required:
            return 'Required parameters: ' + str(n_required) + \
                   ' Order: ' + ' '.join(params_list) + \
                   ' Number of parameters passed: ' + \
                   str(n_params_passed), True
        # else n_params_passed >= n_required
        str_params = '?'
        cont = 0
        for param in alist[level:]:
            str_params = str_params + params_list[cont] + '=' + \
                         param + '&'
            cont += 1
        str_params = str_params[:-1]  # Take off last '&'

    url = url + str_params
    response_text = urlopen(url).read()
    try:
        resposta = response_text.decode('utf-8')
    except AttributeError:
        resposta = response_text
    json_resposta = json.loads(resposta)
    str_resposta = ""
    print(json_resposta)
    if isinstance(json_resposta, list):
        for linha in json_resposta:
            for key, value in linha.items():
                str_resposta = str_resposta + key + ': ' + str(value) + ' \n '
    else:
        for key, value in json_resposta.items():
            str_resposta = str_resposta + key + ': ' + str(value) + ' \n '

    return str_resposta, False
