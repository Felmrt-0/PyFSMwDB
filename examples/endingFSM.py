from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM

def func1():
    print("This is number one")
    return int(input("Nr: "))   # if this returns "2" the FSM moves to State 2

def func2():
    print("This is number two")
    return int(input("Nr: "))   # if this returns "1" the FSM moves to State 1, if it returns "3" it moves to State 3

def func3():
    print("This is the third and final one")
    return "bzzt"   # The return value does not matter since State 3 is an ending


if __name__ == "__main__":
    fsm = FSM()

    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)  # This state is defined as being an ending

    fsm.add_states([state1, state2, state3])

    state1.add_transition(2, state2)    # Setting the transitions seen in the diagram
    state2.add_transition(1, state1)
    state2.add_transition(3, state3)

    fsm.run()