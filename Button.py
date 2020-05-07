class Button:
    state = {}

    def __init__(self, code):
        self.__code = code

    def is_pressed(self):
        return self.state.get(self.__code) is True
