from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM
from PyFSMwDB.Logic import Logic

def func1():
    print("This is number one")
    return int(input("Nr: "))

def func2():
    print("This is number two")
    return int(input("Nr: ")) 

def func3():
    print("This is the third and final one")
    return "bzzt"   # The return value does not matter since State 3 is an ending


if __name__ == "__main__":
    fsm = FSM()

    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)

    fsm.add_states([state1, state2, state3])

    # here the logic for each of the swapping conditions get declared
    logic1_State1 = Logic()
    logic1_State2 = Logic()
    logic2_State2 = Logic()
    logic1_State1.greater_than_limit(5)
    logic1_State2.less_than_limit(4)
    logic2_State2.in_range_limits(4, 8)

    # the logic declared above now gets added as the swapping conditions for the states
    state1.add_transition(logic1_State1, state2)
    state2.add_transition(logic1_State2, state1)
    state2.add_transition(logic2_State2, state3)

    fsm.run()