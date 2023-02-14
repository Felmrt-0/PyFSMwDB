import math

from finite_state_machine_lib.FSM import FSM
from finite_state_machine_lib.State import State
from finite_state_machine_lib.Logic import Logic
import datetime
import time
from termcolor import colored   # do not add termcolor to project requirements

def locked():
    inp = input(colored("It's locked", "red"))
    if inp != "push" and inp != "coin":
        return
    return inp

def unlocked():
    inp = input(colored("It's unlocked", "green"))
    if inp != "push" and inp != "coin":
        return
    return inp

def turnstile():
    print(colored("Running turnstile", "blue"))
    print("Press Enter")
    _ = input()
    fsm = FSM()
    lockedState = State(locked)
    unlockedState = State(unlocked)
    lockedState.add_transition("coin", unlockedState)
    lockedState.add_transition("push", lockedState)
    unlockedState.add_transition("push", lockedState)
    unlockedState.add_transition("coin", unlockedState)
    fsm.add_states([lockedState, unlockedState])
    fsm.set_current_state(lockedState)
    try:
        fsm.run()
    except Exception:
        print(colored("Returned an exception\n", "red"))

def func1():
    print("This is number one")
    return int(input("Nr: "))

def func2():
    print("This is number two")
    return int(input("Nr: "))

def func3():
    print("This is the third and final one\n")
    return "bzzt"

def basicTest():
    print(colored("Running basicTest", "blue"))
    print("Press Enter")
    _ = input()
    fsm = FSM()
    state1 = State(func1)
    state2 = State(func2)
    state3 = State(func3, ending=True)
    fsm.add_states([state1, state2, state3])
    state1.add_transition(2, state2)
    state2.add_transition(3, state3)
    state2.add_transition(1, state1)
    fsm.run()

def arg1(arg):
    val = arg + 1
    print("Your value plus one is", colored(str(val), "red"), end="")
    _ = input()
    return True, val

def arg2(arg):
    val = arg + 1
    print("Your value plus two is", colored(str(val), "red"))

def argTest():
    print(colored("Running argTest", "blue"))
    print("Press Enter")
    _ = input()
    inp = input("Enter a number: ")
    while True:
        try:
            inp = int(inp)
            break
        except ValueError:
            inp = input("No, a number: ")
    fsm = FSM()
    state1 = State(arg1)
    state2 = State(arg2, ending=True)
    state1.add_transition(True, state2)
    fsm.add_states([state1, state2])
    fsm.run(inp)

def dbWrite(db, table: str):
    print("You're in the write function\nEnter a number into database: ", end="")
    inp = input()
    data = {
        "measurement": table,
        "tags": {
            "Info": "Test"
        },
        "time": datetime.datetime.now(),
        "fields": {
            "Input": inp
        }
    }
    db.insert([data])
    return 1, table

def dbRead(db, table: str):
    print("You're in the read function")
    col, data = db.get_latest_rows(table, number_of_rows=1)
    index : int
    for i, c in enumerate(col):
        if c == "Input":
            index = i
            break
    try:
        print("The square root of", colored(str(data[0][index]), "red"), "is", colored(str(math.sqrt(float(data[0][index]))), "red"))
    except ValueError:
        print("The string you entered was", colored(str(data[0][index]), "red"))
    print("The whole table is: ")
    _ = input()
    print(db.print_everything(table))

def dbTest():
    print(colored("Running dbTest", "blue"))
    print("Press Enter")
    _ = input()
    fsm = FSM()
    fsm.create_database()

    state1 = State(dbWrite, static_parameter=fsm.get_database())
    state2 = State(dbRead, static_parameter=fsm.get_database(), ending=True)
    state1.add_transition(1, state2)
    fsm.add_states([state1, state2])
    fsm.run(inp="DemoTable")

class SpeedT:
    @staticmethod
    def farg(inp):
        if isinstance(inp, list):
            current = inp[1]
            max = inp[0]
        else:
            current = 1
            max = inp
        if current <= max:
            return True, max, current+1
        return False

    @staticmethod
    def fdb(db, max=None):
        table = "SpeedT"
        if max is not None:
            current = 1
            data = {
                "measurement": table,
                "time": datetime.datetime.now(),
                "fields": {
                    "Current": current,
                    "Max": max
                }
            }
            db.insert([data])
            return True
        else:
            col, data = db.get_latest_rows(table, number_of_rows=1)
            cur, m = None, None
            for i, c in enumerate(col):
                if c == "Current":
                    cur = i
                elif c == "Max":
                    m = i
                if cur is not None and m is not None:
                    break

            current = data[0][cur]
            max = data[0][m]
            if current <= max:
                data = {
                    "measurement": table,
                    "time": datetime.datetime.now(),
                    "fields": {
                        "Current": current+1,
                        "Max" : max
                    }
                }
                db.insert([data])
                return True
            return False

    @staticmethod
    def endNode():
        return

def speedTest():
    print(colored("Running speedTest", "blue"))
    loops = int(input("Enter how many loops to run: "))
    #loops = inp

    fsmArg = FSM()
    state1 = State(SpeedT.farg)
    endState = State(SpeedT.endNode, ending=True)
    state1.add_transition(True, state1)
    state1.add_transition(False, endState)
    fsmArg.add_states([state1, endState])
    fsmArg.set_current_state(state1)

    startTimeArg = time.time()
    fsmArg.run(loops)
    stopTimeArg = time.time()

    print("Arguments took", colored(str(stopTimeArg-startTimeArg) + " sek", "red"))

    fsmDB = FSM()
    fsmDB.create_database()
    state1 = State(SpeedT.fdb, static_parameter=fsmDB.get_database())
    endState = State(SpeedT.endNode, ending=True)
    state1.add_transition(True, state1)
    state1.add_transition(False, endState)
    fsmDB.add_states([state1, endState])
    fsmDB.set_current_state(state1)

    startTimeDB = time.time()
    fsmDB.run(loops)
    stopTimeDB = time.time()

    print("Database took", colored(str(stopTimeDB-startTimeDB) + " sek", "red"))


    if input("Clear table? [Y/N]").lower() == "y":
        fsmDB.get_database().custom_query("DELETE WHERE time > 0")
        print("Cleared")

class Nestling:
    @staticmethod
    def fMain1(db, table):
        print("You're in state" + colored(" main 1", "green"))
        inp = input("Write an entry: ")
        data = {
            "measurement": table,
            "tags": {
                "Info": "Test"
            },
            "time": datetime.datetime.now(),
            "fields": {
                "Main FSM": inp
            }
        }
        db.insert([data])
        print()
        return True, table

    @staticmethod
    def fSub1(db, table):
        print("  You're in state" + colored(" sub 1", "yellow"))
        col, data = db.get_latest_rows(table, number_of_rows=1)
        index: int
        for i, c in enumerate(col):
            if c == "Main FSM":
                index = i
                break
        print("  The string you entered was", colored(str(data[0][index]), "red"))
        print()
        return True, table

    @staticmethod
    def fSub2(db, table):
        print("  You're in state" + colored(" sub 2", "yellow"))
        inp = input("  Write another entry: ")
        data = {
            "measurement": table,
            "tags": {
                "Info": "Test"
            },
            "time": datetime.datetime.now(),
            "fields": {
                "Sub FSM": inp
            }
        }
        db.insert([data])
        print()
        return True, table

    @staticmethod
    def fMain2(db, table):
        print("You're in state" + colored(" main 2", "green"))
        col, data = db.get_latest_rows(table, number_of_rows=1)
        index: int
        for i, c in enumerate(col):
            if c == "Sub FSM":
                index = i
                break
        print("The string you entered was", colored(str(data[0][index]), "red"))

def nestedTest():
    fsmMain = FSM()
    fsmMain.create_database()
    db = fsmMain.get_database()
    stateM1 = State(Nestling.fMain1, static_parameter=db)

    fsmSub = FSM()
    stateS1 = State(Nestling.fSub1, static_parameter=db)
    stateS2 = State(Nestling.fSub2, static_parameter=db, ending=True)
    stateS1.add_transition(True, stateS2)
    stateSubFSM = State(fsmSub.run)
    fsmSub.add_states([stateS1, stateS2])

    stateM2 = State(Nestling.fMain2, static_parameter=db, ending=True)
    stateM1.add_transition(True, stateSubFSM)
    stateSubFSM.add_transition(True, stateM2)
    fsmMain.add_states([stateM1, stateSubFSM, stateM2])
    fsmMain.run("NestTable")


if __name__ == "__main__":

    inp = input("Enter test nr: ")
    print()
    match inp:
        case "1":
            turnstile()

        case "2":
            basicTest()

        case "3":
            argTest()

        case "4":
            dbTest()

        case "5":
            speedTest()

        case "6":
            nestedTest()

        case other:
            turnstile()
            _ = input()
            basicTest()
            _ = input()
            argTest()
            _ = input()
            dbTest()
            _ = input()
            speedTest()
            _ = input()
            nestedTest()
