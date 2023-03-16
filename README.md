# D0020E-Project
This is a project for the course "Project in Computer Science and 
Engineering" at Luleå University of Technology (Course code: D0020E)

The Project was to create a framework for nessled a Finite-state 
machine (FSM) that could also make use of a database. This framework would then be used 
for another project that has the goal to automize a wheel loader. 

# Requirements
InfluxDB is needed in order to run with the default database. In addition to the python library (installed automatically) the database itself needs to be installed. 

## Linux
```bash
sudo apt install influxdb
```

## Windows
I don't know

## Mac
I don't care

# Installation
Install the .whl file through pip

# How to Use the Framework
After the framework has been installed the first step towards learning to use the framework is to 
read about the functions included in the different classes. This can be done by opening python in a terminal and
writing the following:
```
print(help(*name of class or function*))
```
So for an example, if you want to learn more about the *Logic* class you would write:
```
print(help(Logic))
```
and if you want to learn more about a specific function in the class such as *custom_logic* you would write:
```
print(help(Logic.custom_logic))
```

This can be done for all classes and all public functions in the framework. It is recommended that
you use this to look through the documentation to get a overview of how the different parts of the
framework functions.

What will follow are some examples meant to demonstrate the different use cases of the framework
and how the different use cases can function together. 

## Creating a simple FSM

Before creating a FSM using the framework it is often a good idea to first make a image of the FSM so that you get
a good idea of what states are going to be needed and swapping conditions are going to be used.

For this example the different states of a turnstile is going to be turned into a FSM. The FSM diagram of a turnstile
can be seen in the image below:

![Turnstile FSM digram](https://drive.google.com/uc?export=view&id=1xBTDwIRh0UA7gpBM_U2iEmA4S8pEegiA)

To create this FSM using the frame work the FSM, states and swapping constions need to be declared. An example of how this can be done is shown in the code below. In the example input is provided by the user.

```
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
```

In the code above two states are created `lockedState = State(locked)` and `unlockedState = State(unlocked)`.
As parameters for the *State* two functions are passed, these functions are what is going handle the logic of what
the FSM does when it enters the state. Since this is just an example the functions are going to return either "coin"
or "push" depenting on the users input. If the user input is anything beyond "coin" or "push" the FSM is going to return a exception. The code for *locked* and *unlocked* can be seen below.

```
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
```

## Creating an ending

The example with the turnstile is a FSM that does not have a ending. This means that unless the framework runs in to some problem where a swapping condition is not meet (in the example above this would be the user inputing anything beyond "push" or "coin") the program will run forever.

In many FSM you will want to have some state that the machine can reach where the program will end on its own. An example of such a FSM can be seen in the diagram below.

![FSM diagram with an ending](https://drive.google.com/uc?export=view&id=1mK2-yQa8BgmnOQQiumXZh2NQZYmgOADM)

The diagram shows three states, just like the example with the turnstile the first two states function as an infinite loop. What makes this diagram different is that if **State 2** swaps over to **State 3** the program will finish.

An example of how the code for the FSM would look can be seen below. Like the previous example the input is provided by the user.

```
fsm = FSM()

state1 = State(func1)
state2 = State(func2)
state3 = State(func3, ending=True)  # This state is defined as being an ending

fsm.add_states([state1, state2, state3])

state1.add_transition(2, state2)    # Setting the transitions seen in the diagram
state2.add_transition(1, state1)
state2.add_transition(3, state3)

fsm.run()
```

The three functions can be written as seen below.

```
def func1():
    print("This is number one")
    return int(input("Nr: "))   # if this returns "2" the FSM moves to State 2

def func2():
    print("This is number two")
    return int(input("Nr: "))   # if this returns "1" the FSM moves to State 1, if it returns "3" it moves to State 3

def func3():
    print("This is the third and final one")
    return "bzzt"   # The return value does not matter since State 3 is an ending
```

## Using the Logic class

In the previous two examples all of the swapping conditions have been constant values but when creating FSMs there are cases where the swapping condition is not going to be a constant value. This could be a swapping condition that needs to check if the value returned by a function is greater than a fixed value.

This is where the Logic class is used, when creating swapping conditions such as *greater-than*, *less-than*, *in-range* and *not equal*. An example on how to use *greater-than* and *less-than* can be seen in the FSM diagram below.

![FSM diagram using mathematical inequality and a integer interval](https://drive.google.com/uc?export=view&id=1cczmuFB5yEk9GgFpHXsmxEQcGB48XDjr)

The diagram above is very similar to the one used in the previous example, the difference being that this diagram has swapping condition using mathematical inequality and a integer interval. In the swapping condition between **State 1** and **State 2** it checks if the return value from **State 1** is greater than 5 and the swapping condition between **State 2** and **State 1** is if the return value from **State 2** is less than 4. In order for the FSM to reach the **State 3** which is an ending **State 2** needs to return a integer between 4 and 8.

An example of how the code for the FSM would look can be seen below, the functions are the same as the example above. Like the previous example the input is provided by the user.

```
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
```

### Using custom_logic

**custom_logic** was created it easy to create FSM with very specific swapping conditions. Since **custom_logic** is intended to take into account many different conditions at the same time it is possible that this function contains some strange bugs. We have tried to test for as many cases as possible but it is still very possible that there are cases that causes the function to work incorrectly. 

Because of this you should not use **custom_logic** for any cases where the same result can easily be achieved using the other functions in the Logic class. 

Below an example of a FSM using **custom_logic** can be seen. Just like previous examples input is provided by the user.

![FSM diagram using custom logic](https://drive.google.com/uc?export=view&id=1eLXGhxUAwNnzH9h_xYo7WojUwTBTT33j)

In the diagram there are only two states with one swapping condition. The swapping should be read as follows: switch to State 2 if the return value from State 1 is between 5 and 10, is not equal to 8 or is equal to 15. An example of how the code can be written is seen below.

```
fsm = FSM()

state1 = State(func1)
state2 = State(func2, ending=True)

fsm.add_states([state1, state2])

logic1_State1 = Logic()
logic1_State1.set_custom_logic("< 11, > 4, != 8, = 15")

state1.add_transition(logic1_State1, state2)

fsm.run()
```

The first function is the same `func1` previous examples and the second function is the same as `func3` in previous examples. This means the as long the input from the user fulfills the swapping conditions. The order that the conditions of the custom logic are written in the input string does not matter.

## Passing data between states

When using the FSM it is possible to pass data between the states, meaning that when going from one state to the next you can send data that can be used in the following state. The purpose of being able to send data between states is being able to make a FSM where states are dependent on the values produced in the previous state.

Below an example of a FSM diagram passing arguments between states can be seen. In this example the first value above the arrows is the swapping condition and the second us the arguments being send between the states.

![FSM diagram of data being sent between states](https://drive.google.com/uc?export=view&id=1sr4u0515s5Hdn47IqjjRANxlBkWBjpuu)

As can be seen in the diagram above the swapping conditions for all states will be True since that is not an important part of the test, what is important is the information being sent between the states. An example of how the code can be written is seen below.

```
fsm = FSM()

state1 = State(arg1)
state2 = State(arg2)
state3 = State(arg3, ending=True)

state1.add_transition(True, state2)
state2.add_transition(True, state3)

fsm.add_states([state1, state2, state3])

fsm.run(inp)
```

The argument can be implemented as seen below. They will take a input from the user and increment it by one in each state.

```
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
```

## Using a database

The FSM framework comes with built in support for the time based database InfluxDB. This means that data from the states and values can be saved to a database where its values will be ordered by the time that it was added.

Below an example of a FSM using a database can be seen. Just like previous examples input is provided by the user.

![FSM diagram using a database](https://drive.google.com/uc?export=view&id=1rGHD4sf1Uy7WaFoyPSHb7kDAtSxoUIWU)

In the diagram there are two states with a swapping condition of True. This is because the important part of this example is how the FSM writes and reads data from the database. An example of how the code can be written is seen below.

```
fsm = FSM()
fsm.create_database()

state1 = State(dbWrite, static_parameter=fsm.get_database())
state2 = State(dbRead, static_parameter=fsm.get_database(), ending=True)

state1.add_transition(True, state2)

fsm.add_states([state1, state2])

fsm.run(inp="DemoTable")    # the fsm takes the name of the database as its input
```

The two functions `dbWrite` and `dbRead` handle the writing and reading from the database, an example of how the functions can be written is seen below.

```
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
        print("The square root of your input is: ", str(math.sqrt(data[0][index])))
    except ValueError:
        print("The string entered was", str(data[0][index]))

```

The first function takes a number as input and saves it to the database and the second function reads this value from the database using the function `get_latest_rows` and tries to take the square root of the value. If that fails it will print the string that was entered in the first function.

## Creating a nested FSM

This FSM framework supports nested FSM. This means that all states in the FSM can contain sub-FSMs meaning that you can create FSMs within a FSM. Data can be passed back and forth between the FSM and its sub-FSM. 

Below an example of nested FSM diagram can be seen. In this example the swapping conditions are not specified so it is assumed that all swapping condtions are True.

![Nested FSM diagram](https://drive.google.com/uc?export=view&id=1xYVtLG3tI8DBlvUR40LXSFP2CLyvnq_l)

An example of how the diagram can be constructed in code can be seen below.

```
fsm = FSM()

state1 = State(func1)
state2 = State(func2)
state3 = State(func3, ending=True)

fsm.add_states([state1, state2, state3])

state1.add_transition(True, state2)
state2.add_transition(True, state3)

fsm.run()
```

The code for the states can be seen below. Like previous examples the input is provided by the user, here the input is passed between the states in the FSM and the sub-FSM. 

```
def func1():
    inp = input("Enter a number:")

    while True:
        try:
            inp = int(inp)
            break
        except ValueError:
            inp = input("No, a number:")
    
    return True, inp

def subFunc1(arg):
    print("Your input+1 squared is:", arg*arg)
    return True, arg

def subFunc2(arg):
    sqr = math.sqrt(arg)
    print("The square root of your input+1 is:", sqr)
    return True, sqr

def func2(arg):
    newarg = arg+1
    print("Your input plus one is:", newarg)

    subfsm = FSM()  # create the nested FSM

    subState1 = State(subFunc1, newarg)
    subState2 = State(subFunc2, ending=True)

    subfsm.add_states([subState1, subState2])

    subState1.add_transition(True, subState2)

    sqr = fsm.run()[1]  # get the value from subFunc2

    return True, sqr

def func3(arg):
    print("The squrare root of your input+1 plus one is:", arg+1)

```

The example provided above sends data between the states. Make sure you understand how the data being sent works.

## Using a database in a nested FSM
When working with the framework it is possible to combine the database FSMs with nested FSMs. This means having a FSM with a nested FSM where all states including the sub-states in the nested FSM all write to the same database. An example of this can be seen in the FSM diagram below.

![Diagram of nested FSM with database](https://drive.google.com/uc?export=view&id=1RJnHRhuB3W_kHzRtJ4fnwOURgMfdPrxV)

The swapping conditions between states is True for all the states, this is because the swapping condition does not matter in this example. An example of how the code can be written is seen below.

```
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
```

Below example code for the functions can be seen. The first state will ask for an entry to be written into the database, the first sub-state will read this value, the second sub-state will ask for a new value that will final be read by the third state. This shows that a nested FSM can use the same database as the rest of the FSM.

```
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
            break;
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

    tableReturn = fsm.run(table)[1]  # get the value from subFunc2

    return True, tableReturn

def fMain3(db, table):
    col, data = db.get_latest_rows(table, number_of_rows = 1)
    index: int
    for i, c in enumerate(col):
        if c == "Sub FSM":
            index = i
            break;
    print("The string you entered was ", str(data[0][index]))
    return True, table
```

The example provided above sends data between the states. Make sure you understand how the data being sent works.
