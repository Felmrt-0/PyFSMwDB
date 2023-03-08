from finite_state_machine_lib.State import State
from finite_state_machine_lib.FSM import FSM
from finite_state_machine_lib.Database import Database

test = False
def testFunc():
    global test
    test = True
    return True
def run_test():
    #try:
    test = False
    fsm = FSM()
    state = State(testFunc, ending=True)
    fsm.add_state(state)
    fsm.run()
    if test == True:
        return True
    print("run_test Failed")
    return False
    #except Exception:
    #    print("run_test Failed")
    #    return False
def add_states_test():
    try:
        fsmStates = FSM()
        state1 = State(testFunc)
        state2 = State(testFunc)
        fsmStates.add_states([state1, state2])
        if fsmStates.get_states()[0] == state1 and fsmStates.get_states()[1] == state2:
            return True
        print("add_states_test Failed")
        return False
    except Exception:
        print("add_states_test Failed")
        return False
def set_current_state_test():
    try:
        fsm2 = FSM()
        stateA = State(testFunc)
        fsm2.set_current_state(stateA)
        if fsm2.get_current() == stateA:
            return True
        print("set_current_state_test Failed")
        return False
    except Exception:
        print("set_current_state_test Failed")
        return False

def switch_state_test():
    try:
        fsm3 = FSM()
        stateB = State(testFunc)
        stateC = State(testFunc, ending=True)
        stateB.add_transition(True, stateC)
        fsm3.add_states([stateB, stateC])
        fsm3.run()
        return True
    except Exception:
        print("switch_state_test Failed")
        return False


def set_database_test():
    try:
        fsm4 = FSM()
        fsm4.set_database("root", "root", "DefaultDatabase")
        if fsm4.get_current() == 1:
            return True
        print("set_database_test Failed")
        return False
    except Exception:
        print("set_database_test Failed")
        return False

def create_database_test():
    try:
        fsm5 = FSM()
        fsm5.create_database()
        if fsm5.get_database() != None:
            return True
        print("create_database_test Failed")
        return False
    except Exception:
        print("create_database_test Failed")
        return False

if __name__ == "__main__":
    #run_test()
    add_states_test()
    set_current_state_test()
    switch_state_test()
    set_database_test()
    create_database_test()