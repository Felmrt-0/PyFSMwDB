from Logic import *

#diffrent types of compair varibles
long_compair = 5.12344
double_compair = 5.54
int_compair = 5
float_compair = 5.5
Compare_value = None

def greater_than_limit_unit_test(compare):      #tests if the compaire value = the returned value (__compareValueGreater) from Logic.py
    log = Logic()
    Compare_value = log.greater_than_limit(compare)
    if (Compare_value == compare):
        return print("Looks ok")
    else:
        return print("looks not ok")


def greater_than_limit_unit_test(compare):      #tests if the compaire value = the returned value (__compareValueGreater) from Logic.py
    log = Logic()
    Compare_value = log.greater_than_limit(compare)
    if (Compare_value == compare):
        return print("Looks ok")
    else:
        return print("looks not ok")

def less_than_limit_unit_test(compare):      #tests if the compaire value = the returned value (__compareValueGreater) from Logic.py
    log = Logic()
    Compare_value = log.less_than_limit(compare)
    if (Compare_value == compare):
        return print("Looks ok")
    else:
        return print("looks not ok")

def in_range_limits_unit_test(lower, higher):      #in_range_limits_unit_test from Logic.py. it tries to pass in higher and lower to logic.py otherwise it will cach the exeption.
    log = Logic()
    try: 
        Compare_value_greater = log.in_range_limits(higher,lower)[0]
        Compare_value_Lower = log.in_range_limits(higher,lower)[1]
        if Compare_value_greater > Compare_value_Lower: 
            return print("in_range_limits_unit_test Works fine")
    except Exception: print("The error also works")

def check_string_unit_test(inputstringright, inputstringwrong):
    log = Logic()
    Returnvalue_right = log.get_check_string(inputstringright)
    Returnvalue_wrong = log.get_check_string(inputstringwrong)
    if Returnvalue_right == True:
        print ("works fine with right input")
    if Returnvalue_wrong == False:
        print ("works fine with wrong input (outputs False)")


def set_custom_logic_unit_test(inputtest):
    log = Logic()
    random= "bOIIII" #should raise error 
    Right="<5" #should work fine 
    Rights=" = 5 " #should work fine
    try:
        print("should work:")
        log.set_custom_logic(Right)
        print("should work:")
        log.set_custom_logic(Rights)
        print("should NOT work:")
        log.set_custom_logic(random)    
    except Exception: print("Error works fine")

def in_range_unit_test(input, greater, less):
    log = Logic()
    try:
        log.in_range_limits(greater, less)
        log.in_range(input)
        return print("true (works fine with the inputs)")
    except Exception: print("Error works fine")

def custom_logic_unit_test(custom_logic,input):
    log = Logic()
    log.set_custom_logic(custom_logic)
    print("test custom logic:", log.custom_logic(input))


#def __set_values_unit_test(input):


#greater_than_limit_unit_test(15)
#greater_than_limit_unit_test(long_compair) # works for both float and int
#less_than_limit_unit_test(15)
#less_than_limit_unit_test(long_compair)


#in_range_limits_unit_test(11,12) # testing both the error and also the correkt way to pass in the input
#in_range_limits_unit_test(15,11)
#check_string_unit_test("<", "my name is jeff")
#set_values_unit_test("<2", ">0") #only works with <number  >number =number !=number 

#check_string_unit_test("<2", "BOI0")
#print("-------------------")
#check_string_unit_test("<2", "!!!0")   #one problem is when you give in right input types but in weird formation

#set_custom_logic_unit_test()  

#in_range_unit_test("5", "1", "10") #works with string
#in_range_unit_test(5, 1, 10)    
#in_range_unit_test(5, 2, 1)


#custom_logic_unit_test("= 52, = 76, < 11, > 3, != 9, != 5",7) # works fine
#custom_logic_unit_test("= 52, = 76, < 11, > 3, !!!!= 9, != 5",9)   #ignores the !!!!= 9