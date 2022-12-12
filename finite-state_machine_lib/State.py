from Logic import *

class State:
    def __init__(self, function, name=None, ending=False):
        self.__function = function
        self.__name = name
        self.__ending = ending
        self.__connections = {}

    def add_transition(self, condition, target):
        self.__connections[condition] = target

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_transition(self, condition):
        try:
            return self.__connections[condition]
        except KeyError:
            default_case = None
            for key, item in self.__connections.items():
                if isinstance(key, Logic):
                    lower_bound, upper_bound = key.get_type()
                    if lower_bound < condition < upper_bound: # Love u Python <3
                        return item
                    elif key.is_default():
                        default_case = item
            if default_case is not None:
                return default_case
        raise Exception("Transition not found") # maybe create a new Exception

    def run_function(self, inp=None):
        if inp is None:
            res = self.__function()
        else:
            res = self.__function(inp)
        return res

    def is_ending(self):
        return self.__ending
