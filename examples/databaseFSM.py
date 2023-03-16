from PyFSMwDB.Database import Database
from PyFSMwDB.State import State
from PyFSMwDB.FSM import FSM
import datetime
import math

def dbWrite(db, table: str):
    print("Enter a number to be saved in the database: ")
    inp = input()

    data = {
        "measurement": table,
        "tags" : {
            "Info": "Test"
        },
        "time": datetime.datetime.now(),
        "fields": {
            "Input": inp
        }
    }

    db.insert([data])

    return True, table

def dbRead(db, table: str):
    col, data = db.get_latest_rows(table, number_of_rows=1)
    index : int
    for i, c in enumerate(col):
        if c == "Input":
            index = i
            break
    try:
        print("The square root of your input is: ", str(math.sqrt(float(data[0][index]))))
    except ValueError:
        print("The string entered was", str(data[0][index]))

if __name__ == "__main__":
    fsm = FSM()
    fsm.create_database()

    state1 = State(dbWrite, static_parameter=fsm.get_database())
    state2 = State(dbRead, static_parameter=fsm.get_database(), ending=True)

    state1.add_transition(True, state2)

    fsm.add_states([state1, state2])

    fsm.run(inp="DemoTable")    # the fsm takes the name of the database as its input