# See using the commented lines.

from requests import get
from json import loads


def sync():
    print('Started!')
    #print('Loading...')
    #print('----------')
    req = get('https://jsonplaceholder.typicode.com/posts')
    if req.status_code == 200:
        print('----------')
        print(loads(req.text)[0])
        print('----------')
        print('End.')
        #print('----------')
        #print('Loading...')

sync()