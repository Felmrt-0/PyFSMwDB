from finite_state_machine_lib.State import State

def printFunc():
    print("Print function")
    return True

def parameterFunc(arg):
    print(arg)
    return True


# fixa bättre sätt att testa detta i state(som returna en lista med connections)
def addTransition_test():
    """
    Tests if state can create transitions to other states and itself and store it in its connections

    :return: bool of if it passed or not
    """
    stateTrans1 = State(printFunc)
    stateTrans2 = State(printFunc)
    stateTrans1.add_transition("to1", stateTrans1)
    stateTrans1.add_transition("to2", stateTrans2)
    if stateTrans1.has_transition:
        print("addTransition_test Passed")
        return True
    print("addTransition_test Passed")
    return False

def getConnections_test():
    """
    Tests if transitions created by State are saved correctly

    :return: bool of if it passed or not
    """
    stateCon1 = State(printFunc)
    stateCon2 = State(printFunc)
    stateCon1.add_transition("to1", stateCon1)
    stateCon1.add_transition("to2", stateCon2)
    if "to1" in stateCon1.get_connections() and "to2" in stateCon1.get_connections():
        print("getConnections_test Passed")
        return True
    print("getConnections_test Passed")
    return False

def setParameter_test():
    """
    Tests if the set_parameter function in State.py functions correctly

    :return: bool of if it passed or not
    """
    setParamenterState = State(printFunc)
    setParamenterState.set_parameter("test")
    if setParamenterState.get_parameter() == "test":
        print("setParameter_test Passed")
        return True
    print("setParameter_test Passed")
    return False

def getParameter_test():
    """
    Tests if the get_parameter function in State.py functions correctly

    :return: bool of if it passed or not
    """
    getParameterState = State(printFunc, static_parameter="test")
    string = getParameterState.get_parameter()
    if string == "test":
        print("getParameter_test Passed")
        return True
    print("getParameter_test Failed")
    return False

def setName_test():
    """
    Tests if the setName_test function in State.py functions correctly

    :return: bool of if it passed or not
    """
    setNameState = State(printFunc)
    setNameState.set_name("Name")
    if setNameState.get_name() == "Name":
        print("setName_test Passed")
        return True
    print("setName_test Passed")
    return False

def getName_test():
    """
    Tests if the getName_test function in State.py functions correctly

    :return: bool of if it passed or not
    """
    getNameState = State(printFunc, name="Name")
    if getNameState.get_name() == "Name":
        print("getName_test Passed")
        return True
    print("getName_test Passed")
    return False

def getTransition_test():
    """
    Tests if the getTransition_test function in State.py functions correctly

    :return: bool of if it passed or not
    """
    getTransitionState = State(printFunc)
    testState1 = State(printFunc)
    getTransitionState.add_transition(False, testState1)
    getTransitionState.add_transition(True, getTransitionState)
    trans = getTransitionState.get_transition(False)
    trans1 = getTransitionState.get_transition(True)
    if trans == testState1 and trans1 == getTransitionState:
        print("getTransition_test Passed")
        return True
    print("getTransition_test Passed")
    return False

def hasTransition_test():
    """
    Tests if the hasTransition_test function in State.py functions correctly

    :return: bool of if it passed or not
    """
    hasTransState = State(printFunc)
    testState2 = State(printFunc)
    hasTransState.add_transition(False, testState2)
    if hasTransState.has_transition():
        print("hasTransition_test Passed")
        return True
    print("hasTransition_test Failed")
    return False

def runFunction_test():
    """
    Tests if the runFunction_test function in State.py functions correctly

    :return: bool of if it passed or not
    """
    runFuncState = State(printFunc)
    runTest = runFuncState.run_function()
    paraFuncState = State(parameterFunc)
    runTest2 = paraFuncState.run_function("test")
    if runTest == True and runTest2 == True:
        print("runFunction_test Passed")
        return True
    print("runFunction_test Failed")
    return False

def innit_test():
    """
    Tests if __innit__ in State.py functions correctly

    :return: bool of if it passed or not
    """
    stateStaticParameter = State(printFunc, static_parameter=100)
    stateName = State(printFunc, name="testName")
    stateEnding = State(printFunc, ending=True)
    stateAll = State(printFunc, static_parameter=100, name="test", ending=False)

    staticTest = False
    nameTest = False
    endingTest = False
    allTest = False

    if stateStaticParameter.get_parameter() == 100:
        staticTest = True

    if stateName.get_name() == "testName":
        nameTest = True

    if stateEnding.is_ending() == True:
        endingTest = True

    if stateAll.get_function() == printFunc and stateAll.get_name() == "test" and stateAll.get_parameter() == 100 and stateAll.is_ending() == False:
        allTest = True

    if staticTest and nameTest and endingTest and allTest:
        print("innit_test Passed")
        return True
    print("innit_test Failed")
    return False

if __name__ == "__main__":
    innitTest = innit_test()
    runTest = runFunction_test()
    getParaTest = getParameter_test()
    gotConTest = getConnections_test()
    hasTransTest = hasTransition_test()
    getTransTest = getTransition_test()
    getNameTest = getName_test()
    setNameTest = setName_test()
    setParameterTest = setParameter_test()
    addTransitionTest = addTransition_test()

    if innitTest and runTest and hasTransTest and getTransTest and getNameTest and setNameTest and setParameterTest and addTransitionTest and getParaTest and gotConTest:
        print("all test passed")
