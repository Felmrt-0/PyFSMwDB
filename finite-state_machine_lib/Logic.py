import math
from multiprocessing import Condition

class Logic:

    """def __init__(self, gt=-math.inf, lt=math.inf, default=False):
        self.__greater_than = gt if gt is not None else -math.inf
        self.__less_than = lt if lt is not None else math.inf
        self.__custom_logic = None # not sure what to do with this one
        self.__default = default

    def get_type(self):
        return self.__greater_than, self.__less_than

    def is_default(self):
        return self.__default

    def set_gt(self, gt):
        self.__greater_than = gt if gt is not None else -math.inf

    def set_lt(self, lt):
        self.__less_than = lt if lt is not None else math.inf"""

    def __init__(self):
        self.__compareValueGreater = None
        self.__compareValueLess = None
        self.__notEqualValue = []
        self.__EqualValue = []

    def greater_than_limit(self, compare):
        """This function sets the upper limit for the greater than function"""
        self.__compareValueGreater = compare    # set value compare for "InputValue" > compare

    def less_than_limit(self, compare):
        """This function """
        self.__compareValueLess = compare       # set value compare for "InputValue" < compare
    
    def in_range_limits(self, less, greater):
        if (less < greater):
            self.__compareValueLess = less
            self.__compareValueGreater = greater
        else:
            raise Exception("The lower limit for \"in_range\" is larger or equal to the upper limit")
    
    def debugLimits(self):
        return "The current limits: Greater than = ", self.__compareValueGreater, ", Less than = ", self.__compareValueLess
    
    def set_custom_logic(self, stringInput):
        if self.__check_string(stringInput):
            stringFix = stringInput.replace(" ", "")
            stringSplit = stringFix.split(",")
            self.__set_values(stringSplit)
            
            return
        else:
            raise Exception("The custom logic is written incorrectly")

    def __check_string(self, inputV):
        allowed_characters = {"!", "=", "<", ">", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", ","}
        testInput = set(inputV)
        print("String allowed:", allowed_characters.issuperset(testInput))
        return allowed_characters.issuperset(testInput)

    def __set_values(self, stringSplit):
        for x in stringSplit:
            try:
                if x[0] == '=':
                    self.__EqualValue.append(float(x[1:]))
                    print("equal:", self.__EqualValue)
                elif x[0] == '!' and x[1] == '=':
                    self.__notEqualValue.append(float(x[2:]))
                    print("not equal:", self.__notEqualValue)
                elif x[0] == '<':
                    self.__compareValueLess = float(x[1:])
                    print("less:", self.__compareValueLess)
                elif x[0] == '>':
                    self.__compareValueGreater = float(x[1:])
                    print("greater:", self.__compareValueGreater)
            except:
                raise Exception("Formatting of custom logic is incorrect")
        return

    """def Limit_set_GT(self):
        return True if self.__compareValueGreater != None else False

    def Limit_set_LT(self):
        return True if self.__compareValueLess != None else False"""

    def greater_than(self, inputV):
        return True if self.__compareValueGreater is not None and self.__compareValueLess is None and self.__compareValueGreater < inputV else False

    def less_than(self, inputV):
        return True if self.__compareValueLess is not None and self.__compareValueGreater is None and self.__compareValueLess > inputV else False
    
    def in_range(self, inputV):
        if(self.__compareValueLess is not None and self.__compareValueGreater is not None):
            if(self.__compareValueLess < self.__compareValueGreater):
                return True if self.__compareValueGreater is not None and self.__compareValueLess is not None and self.__compareValueGreater >= inputV and self.__compareValueLess <= inputV else False
            else:
                raise Exception("The lower limit for \"in_range\" is larger or equal to the upper limit")

    def custom_logic(self, inputV):
        if inputV in self.__notEqualValue:
            return False
        elif inputV in self.__EqualValue:
            return True
        elif self.__compareValueGreater is not None and self.__compareValueLess is not None:
            return True if inputV > self.__compareValueGreater and inputV < self.__compareValueLess else False


if __name__ == "__main__":
    test = Logic()
    #print(help(test.greater_than_limit))

    """# test for custom logic
    test.set_custom_logic("= 52, = 76, < 11, > 3, != 9, != 5")
    print("test custom logic:", test.custom_logic(5))"""

    """# test for x > num
    test.greater_than_limit(32)
    print("test greater than:", test.greater_than(40))
    test.greater_than_limit(41)
    print("test greater than:", test.greater_than(40))"""

    """# test for x < num
    test.less_than_limit(32)
    print("test less than:", test.less_than(30))
    test.less_than_limit(29)
    print("test less than:", test.less_than(30))"""

    """# test for num1 <= x <= num2
    # test.in_range_limits(5, 2) # throws exception
    test.in_range_limits(2, 5)
    print("test in range:", test.in_range(1), test.in_range(2), test.in_range(3), test.in_range(4), test.in_range(5), test.in_range(6))
    test.in_range_limits(3, 4)
    print("test in range:", test.in_range(1), test.in_range(2), test.in_range(3), test.in_range(4), test.in_range(5), test.in_range(6))"""