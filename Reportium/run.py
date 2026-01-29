from .config import reportium
from common.httpEx import httpEx
from common.loadEx import load
from common.notifEx import notific
from common.ui import uiall, uidates
from FreeSimpleGUI import WIN_CLOSED

class app:

    # @notific.exception
    @staticmethod
    def run():
        if reportium.dir():
            if (mainwindow := uidates.main(assets=reportium.assets())):
                while True:
                    event, values = mainwindow.read()
                    if event == WIN_CLOSED:
                        break
                    if event == 'Enviar':
                        if '--/--/----' not in values.values():
                            mainwindow.Hide()
                            if (info := reportium.info(values)):  
                                reportium.data(values, info)
                    mainwindow.UnHide()

if __name__ == '__main__':
    app.run()
        