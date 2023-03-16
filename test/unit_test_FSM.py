from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM
from PyFSMwDB.Database import Database

test = False


def testFunc():
    global test
    test = True
    return True


def run_test():
    try:
        global test
        test = False
        fsm = FSM()
        state = State(testFunc)
        state2 = State(testFunc, ending=True)
        state.add_transition(True, state2)
        fsm.add_state(state)
        fsm.add_state(state2)
        res = fsm.run()
        assert res
        if test:
            return res
        print("run_test Failed")
        return res
    except Exception:
        print("run_test Failed")
        return False


def add_states_test():
    try:
        fsmStates = FSM()
        state1 = State(testFunc)
        state2 = State(testFunc)
        fsmStates.add_states([state1, state2])
        if fsmStates._get_states()[0] == state1 and fsmStates._get_states()[1] == state2:
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
        if fsm2._get_current() == stateA:
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
        fsm4.set_database("root", "root", "DefaultDatabase")
        tmp = fsm4.get_database()
        if tmp is not None:
            return True
        print("set_database_test Failed")
        return False
    except Exception as e:
        print("set_database_test Failed")
        return False


def create_database_test():
    try:
        fsm5 = FSM()
        fsm5.create_database()
        if fsm5.get_database() is not None:
            return True
        print("create_database_test Failed")
        return False
    except Exception:
        print("create_database_test Failed")
        return False


if __name__ == "__main__":
    run_test()
    add_states_test()
    set_current_state_test()
    switch_state_test()
    set_database_test()
    create_database_test()
