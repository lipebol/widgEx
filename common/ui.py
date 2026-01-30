from .dbEx import config
from .loadEx import load, system
from FreeSimpleGUI import (
    Button, CalendarButton, Column, FolderBrowse, Image, Input, 
    Text, theme, theme_background_color, Window, WIN_CLOSED
)

class uiall:

    theme('DarkGrey11')

    @staticmethod
    def name(uiname: str | None = None):
        if uiname:
            config.envs()
            list(load.envs())
            return load.variable('UINAME', add=uiname)
    
    @staticmethod
    def buttonclose():
        return Button(
            '', image_data=load.variable('LAYOUTALL_BUTTON').encode(), 
            border_width=0, key='Exit', button_color=(theme_background_color())
        )

    @staticmethod
    def generic(**kwargs) -> object:
        if (screen := list(system.screen(kwargs.get('sizes')))):
            button = Button(
                buttonvalue, font='Courier', bind_return_key=True
            ) if (buttonvalue := kwargs.get('button')) else Text('')
            genericwindow = Window(
                load.variable('UINAME'), layout=[
                    [Column([[uiall.buttonclose()]], justification='right')],
                    [Text('')],
                    [
                        Column(
                            [[Text(kwargs.get('message'), font='Courier')]], 
                            justification='center'
                        )
                    ],
                    [Text('')],
                    [Column([[button]], justification='center')],
                    [Text('')],
                ],
                size=(screen[0], screen[2]), resizable=False, grab_anywhere=False, 
                no_titlebar=True, location=(screen[1], screen[3])
            )
            while True:
                event, values = genericwindow.read()
                if event == 'Exit':
                    genericwindow.Hide()
                    break
                if event == buttonvalue:
                    genericwindow.Hide()
                    return True

    @staticmethod
    def choose(
        *, sizes: list = [0.5859375, 0.4166666666666667], assets: list
    ):
        if (screen := list(system.screen(sizes))):
            if not isinstance(assets, list):
                assets = list(assets)
            choosewindow = Window(
                load.variable('UINAME'), icon=assets[0], layout=[
                    [Text('')],
                    [Column([[Image(filename=assets[1])]])],
                    [
                        Column(
                            [[
                                Text(
                                    'Selecione a pasta para salvar o arquivo:', 
                                    font=('Courier', 13)
                                )
                            ]]
                        )
                    ],
                    [Column([[Input(key='dir'), FolderBrowse(font=('Courier', 10))]])],
                    [Text('')],
                    [Button('Salvar', font='Courier', bind_return_key=True)]
                ],
                size=(screen[0], screen[2]), grab_anywhere=True, alpha_channel=.9, 
                element_justification='c', location=(screen[1], screen[3])
            )
            while True:
                event, values = choosewindow.read()
                if event == WIN_CLOSED:
                    break
                if event == 'Salvar':
                    if (savein := values['dir']):
                        return choosewindow, savein


class uidates:

    @staticmethod
    def calendar(id: str, location: tuple) -> list:
        return [ 
            CalendarButton(
                '➤', locale='pt_BR', begin_at_sunday_plus=1, location=location,
                close_when_date_chosen=True, target=id, format='%d/%m/%Y',  
                month_names=(
                    'Janeiro','Fevereiro','Março','Abril','Maio','Junho', 
                    'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'
                ), day_abbreviations=('Dom','Seg','Ter','Qua','Qui','Sex','Sab')
            ), Input('--/--/----', key=id, size=(10,1), font=('Courier', 11))
        ]

    @staticmethod
    def main(
        *, sizes: list = [0.47058823529411764, 0.4166666666666667], assets: list
    ) -> Window:
        if (screen := list(system.screen(sizes))):
            if not isinstance(assets, list):
                assets = list(assets)
            return Window(
                load.variable('UINAME'), icon=assets[0], layout=[ 
                    [Text('')],
                    [Column([[Image(filename=assets[1])]])],
                    [
                        Column([[Text('  Data Inicial  ', font=('Courier', 13))]]),
                        Column([[Text('  Data Final  ', font=('Courier', 13))]])
                    ],
                    [
                        Text(' '), Column(
                            [uidates.calendar('start_date', (screen[1], screen[3]))]
                        ),
                        Text('      '), Column(
                            [uidates.calendar('end_date', (screen[1]*2, screen[3]))]
                        )
                    ],
                    [Text('')], [Button('Enviar', font='Courier', bind_return_key=True)]
                ], size=(screen[0], screen[2]), grab_anywhere=True, alpha_channel=.9, 
                element_justification='c', location=(screen[1], screen[3])
            )
        raise Exception('')