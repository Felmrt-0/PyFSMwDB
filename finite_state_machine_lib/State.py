from finite_state_machine_lib import State
from finite_state_machine_lib.CustomExceptions import TransitionNotFoundException
from finite_state_machine_lib.Logic import Logic

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
    def __init__(self, function, static_parameter=None, name=None, ending:bool = False):
        """
        A function must be specified when creating a state, this function will be run when the state is.
        :param function: this is the function the state is will run when called
        :param static_parameter: if set, this argument will always be given to the function
        :param name: the name of the state, used for debugging
        :param ending: whether the state is an ending or not
        """
        self.__function = function
        self.__static_parameter = static_parameter
        self.__name = name
        self.__ending = ending
        self.__connections = {}


    def add_transition(self, condition, target: State.State):
        """
        Adds a transition to the state. If the condition is met the target will be run next.
        :param condition: the condition for the transition
        :param target: the target for the transition
        :return: None
        """
        self.__connections[condition] = target

    def set_parameter(self, parameter):
        """
        Sets the constant parameter for the state
        :param parameter: the parameter
        :return: None
        """
        self.__static_parameter = parameter

    def get_parameter(self):
        """
        Returns the constant parameter
        :return: the constant parameter
        """
        return self.__static_parameter

    def set_name(self, name):
        """
        Sets the name of the state
        :param name: the new name
        :return: None
        """
        self.__name = name

    def get_name(self):
        """
        Gets the name of the state
        :return: the name of the state
        """
        return self.__name

    def get_transition(self, condition) -> State.State:
        """
        Returns the transition target given its chosen condition.
        :param condition: a condition belonging to the state
        :return: the state the condition points to
        """
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
        raise TransitionNotFoundException(condition, self.__connections)

    def has_transition(self) -> bool:
        """
        Returns whether the state has a transition or not
        :return: False if the state has no transition. True otherwise
        """
        if len(self.__connections) > 0:
            return True
        else:
            return False

    def run_function(self, arg=None):
        """
        Runs the function saved to the state
        :param arg: the input argument to the function
        :return: whatever the function returns
        """
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

    def is_ending(self):
        """
        Returns whether the state is an ending or not.
        :return: True if the state is an ending. False otherwise
        """
        return self.__ending
