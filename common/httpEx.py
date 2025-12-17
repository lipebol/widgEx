from .loadEx import load
from bs4 import BeautifulSoup
from requests import get, post

class httpEx:

    @load.quiet
    @staticmethod
    def response(func):
        def wrapper(**kwargs):
            if (url := kwargs.get('url')):
                load.info(f"Requesting... ({url})")
                __headers = {'User-Agent': load.variable('HEADERS')}
                if (__addheaders := kwargs.get('headers')):
                    __headers = {**__headers, **__addheaders}
                if (
                    response := get(
                        url, params=kwargs.get('params'), timeout=60, headers=__headers
                    ) if not (data := kwargs.get('data')) 
                    else post(url, data=data, headers=__headers, timeout=60)
                ).status_code == 200:
                    kwargs['response'] = response
                    return func(**kwargs)
                raise Exception(response.status_code, response.text)
            raise Exception('URL?')
        return wrapper
    

    @response
    @staticmethod
    def fetch(**kwargs):
        return kwargs.get('response').json()

    @response
    @staticmethod
    def scrape(**kwargs) -> list:
        if not kwargs.get('type'):
            kwargs['type'] = 'lxml'
        if not kwargs.get('tag'):
            kwargs['tag'] = 'a'
        if not kwargs.get('attrs'):
            kwargs['attrs'] = {}
        return BeautifulSoup(
            kwargs.get('response').text, kwargs.get('type') ### <-- 'xml' or 'lxml'
        ).find_all(kwargs.get('tag'), attrs=kwargs.get('attrs'))

    @response
    @staticmethod
    def save(**kwargs):
        if not kwargs.get('filename'):
            kwargs['filename'] = load.path(kwargs.get('url')).name
        with open(
            (
                savein := load.path(
                    kwargs.get('savein'), 
                    join=kwargs.get('filename')
                )
            ), 'wb'
        ) as handler:
            handler.write(kwargs.get('response').content)
        load.info(str(savein))
        
    @staticmethod
    def checkIP(**kwargs):

        @response
        def ip(**kwargs):
            return kwargs.get('response').strip()
        
        if (ipadress := ip(url=load.variable('CHECK_IP'))):
            if not load.checkpath(
                tmpfile := load.tmpfile(path=load.path(join='common'))
            ):
                load.jsonEx(path=tmpfile, data={'ip': ipadress})
            return load.jsonEx(path=tmpfile).get('ip') == ipadress
        