from apps.chat.layout import layout
from core.controller import Controller


class ChatController(Controller):
    def __init__(self):
        Controller.__init__(self, 'chat')
        print('nlp controller init...')

    def layout(self):
        return layout


controller = ChatController()
