from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM

def arg1():
    inp = input("Enter a number: ")
    while True:
        try:
            inp = int(inp)
            break
        except ValueError:
            inp = input("No, a number: ")
    
    return True, inp

def arg2(arg):
    val = arg + 1
    print("Your value plus one is: ", str(val))

    return True, val

def arg3(arg):
    val = arg + 1
    print("Your value plus two is: ", str(val))

if __name__ == "__main__":
    fsm = FSM()

    state1 = State(arg1)
    state2 = State(arg2)
    state3 = State(arg3, ending=True)

    state1.add_transition(True, state2)
    state2.add_transition(True, state3)

    fsm.add_states([state1, state2, state3])

    fsm.run()