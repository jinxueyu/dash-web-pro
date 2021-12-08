from apps.frontend import layout
from core.controller import Controller


class FEController(Controller):
    def __init__(self):
        Controller.__init__(self, 'frontend')

    def index(self):
        return layout.layout()


fe_controller = FEController()
