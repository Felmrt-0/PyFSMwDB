from Database import *
from State import *
from Logic import *

class FSM:
    def __init__(self):
        self.__states = []
        self.__currentState = None
        self.__database = None

    def run(self, inp=None):
        while not self.__currentState.is_ending():
            res = self.__currentState.run_function(inp)
            self.__switch_state(res)
        self.__currentState.run_function(inp) # this is for running the ending module as well

    def __add_state(self, state):
        assert not isinstance(state, list), "The module should not be a list"
        self.__states.append(state)
        if self.__currentState is None:
            self.__currentState = state

    def add_states(self, state):
        assert isinstance(state, list), "The input should be a list"
        for s in state:
            self.__add_state(s)

    def set_current_state(self, state):
        assert not isinstance(state, list), "The module should not be a list"
        self.__currentState = state

    def __switch_state(self, condition):
        self.__currentState = self.__currentState.get_transition(condition)

    def setDatabase(self, name, password,dbName):
        self.__database = Database.setDatabase(name, password, dbName)

    def currentPos(self):
        return "The FSM is currently in module " + self.__currentState.get_name()


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
    lockedState = State.State(locked)
    unlockedState = State.State(unlocked)
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
    def test(state):
        state.cond = True

    state1 = State(test)
    state2 = State(test)

    state1.add_transition(True, state2)
    state2.add_transition(True, state1)



