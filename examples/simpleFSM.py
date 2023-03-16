from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM

def locked():
    inp = input("It's locked")
    if inp != "push" and inp != "coin":
        return
    return inp

def unlocked():
    inp = input("It's unlocked")
    if inp != "push" and inp != "coin":
        return
    return inp

fsm = FSM() # declare the FSM

lockedState = State(locked) # the create the two states seen in the image
unlockedState = State(unlocked) # pass in functions for the states

lockedState.add_transition("coin", unlockedState) # add the four transitions seen in the image
lockedState.add_transition("push", lockedState)
unlockedState.add_transition("push", lockedState)
unlockedState.add_transition("coin", unlockedState)

fsm.add_states([lockedState, unlockedState]) # add the states to the FSM

fsm.set_current_state(lockedState) # set the state that the FSM is going to start in´

fsm.run()