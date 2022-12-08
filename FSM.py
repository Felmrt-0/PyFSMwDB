import math

class FSM:
    def __init__(self):
        self.__states = []
        self.__currentState = None
        self.__done = False

    def run(self, inp=None):
        while not self.__done:
            res = self.__currentState.run_function(inp)
            self.__switch_state(res)
        self.__currentState.run_function(inp)

    def add_state(self, state):
        assert not isinstance(state, list), "The module should not be a list"
        self.__states.append(state)
        if self.__currentState is None:
            self.__currentState = state

    def add_states(self, state):
        assert isinstance(state, list), "The input should be a list"
        for s in state:
            self.add_state(s)

    def set_current_state(self, state):
        assert not isinstance(state, list), "The module should not be a list"
        self.__currentState = state

    def __switch_state(self, condition):
        self.__currentState = self.__currentState.get_transition(condition)
        if self.__currentState.is_ending():
            self.__done = True


class State:
    def __init__(self, function, name=None, ending=False):
        self.__function = function
        self.__name = name
        self.__ending = ending
        self.__connections = {}
        #self.__logics = [greaterthan, 0] # fix this thing

    def add_transition(self, condition, target):
        self.__connections[condition] = target

    def set_name(self, name):
        self.__name = name

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


class Logic:
    def __init__(self, gt=-math.inf, lt=math.inf, default=False):
        self.__greater_than = gt if gt is not None else -math.inf
        self.__less_than = lt if lt is not None else math.inf
        self.__custom_logic = None # not sure what to do with this one
        self.__default = default

    def get_type(self):
        return self.__greater_than, self.__less_than

    def is_default(self):
        return self.__default

    def set_gt(self, gt):
        self.__greater_than = gt if gt is not None else -math.inf

    def set_lt(self, lt):
        self.__less_than = lt if lt is not None else math.inf

def func1():
    print("This is number one")
    return int(input("Nr: "))

def func2():
    print("This is number two")
    return int(input("Nr: "))

def func3():
    print("This is the third and final one")
    return "bzzt"

def locked():
    inp = input("It's locked")
    return inp

def unlocked():
    inp = input("It's unlocked")
    return inp




def basicTest(fsm):
    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(2, state2)
    state2.add_transition(3, state3)

def stringTest(fsm):
    lockedState = State(locked)
    unlockedState = State(unlocked)
    lockedState.add_transition("coin", unlockedState)
    lockedState.add_transition("push", lockedState)
    unlockedState.add_transition("push", lockedState)
    unlockedState.add_transition("coin", unlockedState)
    fsm.add_states([lockedState, unlockedState])
    fsm.set_current_state(unlockedState)

def logicTest(fsm):
    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(Logic(gt=1, lt=5), state2)
    state1.add_transition(Logic(default=True), state3)
    state2.add_transition(Logic(gt=3), state3)

if __name__ == "__main__":
    fsm = FSM()
    # basicTest(fsm)
    # stringTest(fsm)
    logicTest(fsm)

    fsm.run()
