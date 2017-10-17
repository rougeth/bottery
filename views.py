# -*- coding: utf-8 -*-
'''Views customizadas utilizadas neste projeto
São as funcões que geram o conteúdo para a submissão à
API que o Usuário acessa.
'''
import json
import urllib.request


ULRAPP = 'http://brasilico.pythonanywhere.com/'
STATUS = ['OK', 'Divergente', 'Sem Lacre']
END_HOOK_LIST = ['fim', 'end', 'exit', 'sair']

def two_tokens(text):
    '''Receives a text string, splits on first space, return
    first word of list/original sentence and the rest of the sentence
    '''
    lista = text.split(' ')
    return lista[0], " ".join(lista[1:])

def help_text(message):
    '''Retorna a lista de Patterns/ disponíveis'''
    # TODO Fazer modo automatizado
    lstatus = [str(key) + ': ' + value + ' ' for key, value in list(enumerate(STATUS))]
    str_end_hook = ', '.join(END_HOOK_LIST)
    return  ('help - esta tela de ajuda \n'
             'ping - teste, retorna "pong"\n'
            'tec - entra na aplicação TEC \n' + \
            'cep - entra na aplicação CEP \n' + \
            str_end_hook + ' - Sai de uma aplicação \n')


def say_help(message):
    '''Se comando não reconhecido'''
    return 'Não entendi o pedido. \n Digite help para uma lista de comandos.'
