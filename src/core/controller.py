import threading
import time


class Controller(object):
    def __init__(self, name):
        self.name = name
        Controllers.instance().regist(self)


class Controllers(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        print('.controllers..init....')
        self.init()
        time.sleep(1)

    @classmethod
    def instance(cls):
        if not hasattr(Controllers, "_instance"):
            with Controllers._instance_lock:
                if not hasattr(Controllers, "_instance"):
                    Controllers._instance = Controllers()
        return Controllers._instance

    def init(self):
        self.__controllers = {}

    def get(self, name):
        return self.__controllers.get(name, None)

    def regist(self, controller):
        self.__controllers[controller.name] = controller


def get(name):
    return Controllers.instance().get(name)
