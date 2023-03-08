from finite_state_machine_lib.Database import Database
from finite_state_machine_lib.State import State
from finite_state_machine_lib.Logic import Logic


class FSM:
    """
    A class that is used to create a finite-state machine(FSM) that can store states with code within it

    Attributes
    ----------
    states : list
        A list with all the states that exists in the FSM
    currentState : State
        The current state the FSM is running or is using
    done : bool
        A bool that determent if the FSM is done running
    databaste : Database
        A influxdb 2.0 database where you can load and save data

    Methods
    -------
    run( inp = None )
        Runs the current state
    add_state( State )
        Adds a state to the FSM
    add_states( State[] )
        Adds a list of states to the FSM
    set_current_state( State )
        Sets the current state to State
    switch_state( condition )
        Switches the current state in the FSM
    set_database( name, password, dbName)
        sets the database to one that already exists
    create_database()
        Creates a new InfluxDB database
    get_database()
        return self.__database
     """
    def __init__(self):
        self.__states = []
        self.__currentState = None
        self.__done = False
        self.__database = None

    def run(self, inp=None, deadend_check:bool=True):
        """
        It will run the function, save its return value as 'condition' and 'arguement' if any, otherwise just
        'condition'. Condition will decide what module is run next and any argument will be passed to it.
        deadend_check will be passed down to any sub FSMs.

        :param inp: input argument to be sent into the first function
        :param deadend_check: whether a dead-end check will be run before execution
        :return: whatever the last State returns
        """
        if deadend_check:
            assert not self.deadend_check(), "Dead-end detected"
        argument = inp

        while not self.__done:
            if argument is not None:
                res = self.__currentState.run_function(argument)
            else:
                res = self.__currentState.run_function()
            if isinstance(res, list) or isinstance(res, tuple):
                if len(res) == 2:
                    cond, argument = res
                else:
                    cond, *argument = res
            else:
                cond = res
                argument = None
            self.__switch_state(cond)

        if argument is not None:
            return self.__currentState.run_function(argument)
        else:
            return self.__currentState.run_function()

    def deadend_check(self) -> bool:
        """
        Checks the states for dead-ends.

        :return: True if a dead-end is detected, False otherwise
        """
        for s in self.__states:
            if not s.has_transition() and not s.is_ending():
                return True
        return False

    def add_state(self, state: State):
        """
        Adds a state to the FSM's state list

        :param state: this state will be added to a list of states
        :return: None
        """
        assert not isinstance(state, list), "The module should not be a list"
        if isinstance(state, FSM):
            state.__database = self.__database
        self.__states.append(state)
        if self.__currentState is None:
            self.__currentState = state

    def add_states(self, states: list):
        """
        Iterates through the input to add all states into the state list

        :param states: a list of states
        :return: None
        """
        for state in states:
            self.add_state(state)

    def set_current_state(self, state: State):
        """
        Sets the input state as the starting point.
        By default, the first state added to the list will be the starting point.

        :param state: the fsm will start from this state
        :return: None
        """
        assert not isinstance(state, list), "The module should not be a list"
        self.__currentState = state

    def __switch_state(self, condition):
        """
        Updates current state to the next one based one the given condition.
        Sets flag if the new state is and endpoint.

        :param condition: condition to switch state
        :return: None
        """

        self.__currentState = self.__currentState.get_transition(condition)
        if self.__currentState.is_ending():
            self.__done = True

    def set_database(self, name, password, dbName):
        """
        Sets the current database based on the arguments given.

        :param name: the name of the user
        :param password: the password of the user
        :param dbName: the name of the database
        :return: None
        """
        self.__database = Database.set_database(name, password, dbName)

    def create_database(self):
        """
        Creates a Database object and runs its create_database() function.

        :return: None
        """
        self.__database = Database()
        self.__database.create_database()

    def get_database(self) -> Database:
        """
        Returns the current database.

        :return: current database
        """
        return self.__database

    def get_states(self):
        return self.__states

    def get_current(self):
        return self.__currentState

    def is_Done(self):
        return self.__done


def func1():
    print("This is number one")
    return int(input("Nr: "))

def func2():
    print("This is number two")
    return int(input("Nr: "))

def func3():
    print("This is the third and final one")
    return "bzzt"

def locked(database):
    assert isinstance(database, Database)
    inp = input("It's locked")
    data = {
        "measurement": "TestTable",
        "tags": {
            "Info": "Test"
        },
        "time": datetime.datetime.now(),
        "fields": {
            "locked" : inp
        }
    }
    database.insert([data])
    if inp != "push" and inp != "coin":
        return
    return inp, database

def unlocked(database):
    assert isinstance(database, Database)
    inp = input("It's unlocked")
    data = {
        "measurement": "TestTable",
        "tags": {
            "Info": "Test"
        },
        "time": datetime.datetime.now(),
        "fields": {
            "unlocked": inp
        }
    }
    database.insert([data])
    if inp != "push" and inp != "coin":
        return
    return inp, database

def endNode():
    print("Finished")

def basicTest(fsm):
    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(2, state2)
    state2.add_transition(3, state3)

def stringTest(fsm):
    lockedState = State(locked)
    unlockedState = State(unlocked)
    endState = State(endNode, ending=True)
    lockedState.add_transition("coin", unlockedState)
    lockedState.add_transition("push", lockedState)
    unlockedState.add_transition("push", lockedState)
    unlockedState.add_transition("coin", unlockedState)
    lockedState.add_transition(Logic(default=True), endState)
    unlockedState.add_transition(Logic(default=True), endState)
    fsm.add_states([lockedState, unlockedState])
    fsm.set_current_state(lockedState)

def logicTest(fsm):
    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(Logic(gt=1, lt=5), state2)
    state1.add_transition(Logic(default=True), state3)
    state2.add_transition(Logic(gt=3), state3)

def nessledDatabaseTest(fsm):
    fsm.create_database()
    fsm1 = FSM()
    fsm.add_state(fsm1)
    fsm2 = FSM()
    fsm1.add_state(fsm2)
    state = State(testFunction)
    state1 = State(testFunction, ending=True)
    state.add_transition(True, state1)
    fsm2.add_state(state)
    fsm2.add_state(state1)
    fsm.run()

def testFunction():

    print("This is a test function")

if __name__ == "__main__":
    import datetime
    fsm = FSM()
    nessledDatabaseTest(fsm)


