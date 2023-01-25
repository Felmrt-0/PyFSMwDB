from Logic import *

class State:
    """
    A class that creates State objects

    Attributes
    ----------
    function : function
        function that runs when this state runs
    static_parameter:

    name : Str
        Names the state
    ending :

    connections : dict
        Dictunary that connects states to eachother

    Methods
    -------

    """
    def __init__(self, function, static_parameter=None, name=None, ending=False):
        """

        :param function:
        :param static_parameter:
        :param name:
        :param ending:
        """
        self.__function = function
        self.__static_parameter = static_parameter
        self.__name = name
        self.__ending = ending
        self.__connections = {}


    def add_transition(self, condition, target):
        self.__connections[condition] = target

    def set_parameter(self, parameter):
        self.__static_parameter = parameter

    def get_parameter(self):
        return self.__static_parameter

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_transition(self, condition):
        if len(self.__connections) == 1:
            self.__ending = True
            return self
        else:
            try:
                return self.__connections[condition]
            except KeyError:
                default_case = None
                for key, item in self.__connections.items():
                    if isinstance(key, Logic):
                        """lower_bound, upper_bound = key.get_type()
                        if key.is_default():
                            default_case = item
                        elif lower_bound < float(condition) < upper_bound: # Love u Python <3
                            return item"""
                        #if key.in_range(float(condition)) or key.greater_than(float(condition)) or key.less_than(float(condition)):
                        if key.in_range(float(condition)):
                            return item
                        elif key.greater_than(float(condition)) or key.less_than(float(condition)):
                            return item

                if default_case is not None:
                    return default_case
            raise Exception("Transition not found") # maybe create a new Exception

    def has_transition(self):
        if len(self.__connections) > 0:
            return True
        else:
            return False

    def run_function(self, arg=None):
        if self.__static_parameter is None:
            if arg is None:
                res = self.__function()
            else:
                res = self.__function(arg)
        else:
            if arg is None:
                res = self.__function(self.__static_parameter)
            else:
                res = self.__function(self.__static_parameter, arg)
        return res
    def isLastInList(self):
        return list(self.__connections)[-1]
    def is_ending(self):
        return self.__ending
