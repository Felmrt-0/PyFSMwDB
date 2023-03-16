from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM
from PyFSMwDB.Logic import Logic

def func1():
    print("This is number one")
    return int(input("Nr: "))

def func2():
    print("This is the second and final one")
    return "bzzt"   # The return value does not matter since State 2 is an ending


if __name__ == "__main__":
    fsm = FSM()

    state1 = State(func1)
    state2 = State(func2, ending=True)

    fsm.add_states([state1, state2])

    logic1_State1 = Logic()
    logic1_State1.set_custom_logic("< 11, > 4, != 8, = 15")

    state1.add_transition(logic1_State1, state2)

    fsm.run()