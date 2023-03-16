from PyFSMwDB.State import State
from PyFSMwDB.Database import Database
from PyFSMwDB.FSM import FSM
import datetime
import math

def fMain1(db, table):
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
    return True, table

def fSub1(db, table):
    col, data = db.get_latest_rows(table, number_of_rows = 1)
    index: int
    for i, c in enumerate(col):
        if c == "Main FSM":
            index = i
            break
    print("The string you entered was ", str(data[0][index]))
    return True, table

def fSub2(db, table):
    inp = input("Write another entry: ")
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
    return True, table

def fMain2(db, table):
    subfsm = FSM()  # create the nested FSM

    subState1 = State(fSub1, static_parameter=db)
    subState2 = State(fSub2, static_parameter=db, ending=True)

    subfsm.add_states([subState1, subState2])

    subState1.add_transition(True, subState2)

    tableReturn = subfsm.run(table)[1]  # get the value from subFunc2

    return True, tableReturn

def fMain3(db, table):
    col, data = db.get_latest_rows(table, number_of_rows = 1)
    index: int
    for i, c in enumerate(col):
        if c == "Sub FSM":
            index = i
            break
    print("The string you entered was ", str(data[0][index]))
    return True, table

if __name__ == "__main__":
    # create the main FSM
    fsmMain = FSM()

    fsmMain.create_database()
    db = fsmMain.get_database()

    state1 = State(fMain1, static_parameter=db)
    state2 = State(fMain2, static_parameter=db)
    state3 = State(fMain3, static_parameter=db, ending=True)

    fsmMain.add_states([state1, state2, state3])

    state1.add_transition(True, state2)
    state2.add_transition(True, state3)

    fsmMain.run("NestTable")    # name of table