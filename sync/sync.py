# Veja utilizando as linhas comentadas.

from requests import get
from json import loads


def sync():
    print('Começou!')
    #print('Aguardando...')
    #print('----------')
    req = get('https://jsonplaceholder.typicode.com/posts')
    if req.status_code == 200:
        print('----------')
        print(loads(req.text)[0])
        print('----------')
        print('Terminou.')
        #print('----------')
        #print('Aguardando...')

sync()