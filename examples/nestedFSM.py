from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM
import math

def func1():
    inp = input("Enter a number:")

    while True:
        try:
            inp = int(inp)
            break
        except ValueError:
            inp = input("No, a number:")
    
    return True, inp

def subFunc1(arg):
    print("  Your input+1 squared is:", arg*arg)
    return True, arg

def subFunc2(arg):
    sqr = math.sqrt(arg)
    print("  The square root of your input+1 is:", sqr)
    return True, sqr

def func2(arg):
    newarg = arg+1
    print("Your input plus one is:", newarg)

    subfsm = FSM()  # create the nested FSM

    subState1 = State(subFunc1, newarg)
    subState2 = State(subFunc2, ending=True)

    subfsm.add_states([subState1, subState2])

    subState1.add_transition(True, subState2)

    sqr = subfsm.run()[1]  # get the value from subFunc2

    return True, sqr

def func3(arg):
    print("The squrare root of your input+1 plus one is:", arg+1)


if __name__ == "__main__":
    fsm = FSM()

    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)

    fsm.add_states([state1, state2, state3])

    state1.add_transition(True, state2)
    state2.add_transition(True, state3)

    fsm.run()