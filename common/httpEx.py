from .loadEx import load
from bs4 import BeautifulSoup
from requests import get

class httpEx:

    @load.quiet
    @staticmethod
    def getdata(func):
        def wrapper(**kwargs):
            if (url := kwargs.get('url')):
                load.info(f"Requesting... ({url})")
                if (
                    response := get(
                        url, params=kwargs.get('params'), timeout=30, 
                        headers={'User-Agent': load.variable('HEADERS')}
                    )
                ).status_code == 200:
                    kwargs['response'] = response.text
                    return func(**kwargs)
                raise Exception(response.status_code, response.text)
            raise Exception('URL?')
        return wrapper
    
    @getdata
    @staticmethod
    def scrape(**kwargs) -> list:
        if not kwargs.get('type'):
            kwargs['type'] = 'lxml'
        if not kwargs.get('tag'):
            kwargs['tag'] = 'a'
        if not kwargs.get('attrs'):
            kwargs['attrs'] = {}
        return BeautifulSoup(
            kwargs.get('response'), kwargs.get('type') ### <-- 'xml' or 'lxml'
        ).find_all(kwargs.get('tag'), attrs=kwargs.get('attrs'))
        
    @staticmethod
    def checkIP(**kwargs):

        @httpEx.getdata
        def ip(**kwargs):
            return kwargs.get('response').strip()
        
        if (ipadress := ip(url=load.variable('CHECK_IP'))):
            if not load.checkpath(
                tmpfile := load.tmpfile(path=load.path(join='common'))
            ):
                load.jsonEx(path=tmpfile, data={'ip': ipadress})
            return load.jsonEx(path=tmpfile).get('ip') == ipadress
        