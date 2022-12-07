
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
            for key, item in self.__connections:
                # do something with logic
                pass
        raise Exception("Transition not found")

    def run_function(self, inp=None):
        if inp is None:
            res = self.__function()
        else:
            res = self.__function(inp)
        return res

    def is_ending(self):
        return self.__ending


class Logic:
    # solve the problem of default case from the State class

    # this is just a stub, nothing is decided yet
    def less_than(self):
        pass

    def greater_than(self):
        pass

    def custom_logic(self):
        pass


def func1():
    print("This is number one")
    return 2

def func2():
    print("This is number two")
    return 3

def func3():
    print("This is the third and final one")
    return "bzzt"

def locked():
    inp = input("It's locked")
    return inp

def unlocked():
    inp = input("It's unlocked")
    return inp

if __name__ == "__main__":
    fsm = FSM()
    """state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending = True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(2, state2)
    state2.add_transition(3, state3)"""

    lockedState = State(locked)
    unlockedState = State(unlocked)
    lockedState.add_transition("coin", unlockedState)
    lockedState.add_transition("push", lockedState)
    unlockedState.add_transition("push", lockedState)
    unlockedState.add_transition("coin", unlockedState)
    fsm.add_states([lockedState, unlockedState])
    fsm.set_current_state(unlockedState)

    fsm.run()
