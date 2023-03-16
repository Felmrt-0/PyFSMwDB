from PyFSMwDB.CustomExceptions import LogicException, CustomLogicException


class Logic:
    """
    A class used for creating logical expressions

    Attributes
    ----------
    customLogic : bool
        set to True when custom logic is used

    compareValueGreater: int float douable
        Greater value

    compareValueLess : int float double
        Lesser value

    notEqualValue : list
        not Equal

    EqualValue : list
        Dictunary that connects states to each other

    Methods
    -------
    greater_than_limit(compare)
        Sets the value that the input value will be compared to in a "greater than" operation.

    less_than_limit(compare)
        Sets the value that the input value will be compared to in a "less than" operation.

    in_range_limits(less, greater)
        Sets the limits for the input value in a "in range" operation.

    debugLimits()
        Returns all values currently saved as comparison values as a string. Used for debugging.

    set_custom_logic(stringInput)
        Sets the logic for a "custom logic" operation.

    greater_than(inputV)
        Returns True if the input value is greater than the upper limit that has been set. A lower limit can NOT be set when using this function.

    less_than(inputV)
        Returns True if the input value is less than the lower limit that has been set. A upper limit can NOT be set when using this function.

    in_range(inputV)
        Returns True if the input value is within the limits that have been set.

    custom_logic(inputV)
        Returns True if the input value fulfills the logic that was set in "set_custom_logic".

    set___compareValueGreater()
        Sets value for self.__compareValueGreater

    set___compareValueGreater(greater)
        Sets value for self.__compareValueGreater

    set___compareValueLess(less)
        Sets value for self.__compareValueLess

    get_check_string(input)
        Fetches check_string for input

    get___compareValueGreater()
        get___compareValueGreater

    get__compareValueLess()
        Fetches __compareValueLess

    get__notEqualValue()
        Fetches __notEqualValue

    get__EqualValue()
        Fetches __EqualValue

    """

    #def __init__(self, logic=False):
    def __init__(self, logic=False):
       self.customLogic = logic  # set true when using custom logic
       self.__compareValueGreater = None
       self.__compareValueLess = None
       self.__notEqualValue = []
       self.__EqualValue = []


    def greater_than_limit(self, compare):
        """
        This function sets the upper limit for the greater than function

        :param Compare: The value that the input value in the "greater_than" function will be compared to.
        :return: self.__compareValueGreater
        """
        self.__compareValueGreater = compare    # set value compare for "InputValue" > compare
        return self.__compareValueGreater       # return for unit test 

    def less_than_limit(self, compare):
        """
        This function sets the lower limit for the lower than function

        :param compare: The value that the input value in the "less_than" function will be compared to.
        :return: self.__compareValueLess
        """
        self.__compareValueLess = compare       # set value compare for "InputValue" < compare
        return self.__compareValueLess
    
    def in_range_limits(self, less, greater):
        """
        This function sets the lower and upper limit for a in range function 

        :param less: The lower value in the in range operation.
        :param greater: The greater value in the in range operation.
        :raise LogicException: The lower limit for in_range is larger or equal to the upper limit
        :return: greater, less
        """
        if (less < greater):
            self.__compareValueLess = less
            self.__compareValueGreater = greater
            return greater, less
        else:
            raise LogicException("The lower limit for \"in_range\" is larger or equal to the upper limit")
    
    
    def debugLimits(self):
        """
        This functions returns a string with all values saved in the class

        :return:  String with all values saved in the class
        """
        return "The current limits: Greater than = ", self.__compareValueGreater, ", Less than = ", self.__compareValueLess
    
    def set_custom_logic(self, stringInput):
        """
        This function allows users to set their own logic

        :param stringInput: The string that will contain the "custom logic"
        :raise CustomLogicException: The custom logic is written incorrectly, the stringInput contains characters that are not: "!", "=", "<", ">", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", ","
        :return: None
        """
        if self.__check_string(stringInput):
            stringFix = stringInput.replace(" ", "")
            stringSplit = stringFix.split(",")
            self.__set_values(stringSplit)
            return 
        else:
            raise CustomLogicException("The custom logic is written incorrectly")

    # makes sure that the input string in set_custom_logic only contains characters that are allowed
    def __check_string(self, inputV):
        """
        Checks if String is allowed

        :param inputV:
        :return:
        """
        allowed_characters = {"!", "=", "<", ">", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", ","}
        testInput = set(inputV)
        print("String allowed:", allowed_characters.issuperset(testInput))
        return allowed_characters.issuperset(testInput)



    # takes the input string from set_custom_logic and turns it into values that can be saved in the class
    def __set_values(self, stringSplit):
        """


        :param stringSplit:
        :raise CustomLogicException: Formatting of custom logic is incorrect
        :return: self.__EqualValue
        """
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
                raise CustomLogicException("Formatting of custom logic is incorrect")
        return self.__EqualValue
    

    def greater_than(self, inputV):
        """
        This function returns True if the greater than limit is less than the input value. The less than limit can NOT be set when using this function.

        :param inputV: The value that will be compared to the value set during the set_greater_than operation
        :return: True if self.__compareValueGreater is not None and self.__compareValueLess is None and self.__compareValueGreater < inputV else False
        """
        return True if self.__compareValueGreater is not None and self.__compareValueLess is None and self.__compareValueGreater < inputV else False

    def less_than(self, inputV):
        """
        This function returns True if the less than limit is more than the input value. The more than limit can NOT be set when using this function.

        :param inputV: The value that will be compared to the value set during the set_less_than operation
        :return: True if self.__compareValueLess is not None and self.__compareValueGreater is None and self.__compareValueLess > inputV else False
        """
        return True if self.__compareValueLess is not None and self.__compareValueGreater is None and self.__compareValueLess > inputV else False
    
    def in_range(self, inputV):
        """
        This function returns True if the input value is between the upper and lower bound.

        :param inputV: The value that will be compared to the values set during the set_in_range operation
        :raise LogicException: The lower limit for in_range is larger or equal to the upper limit
        :return: True if self.__compareValueGreater >= inputV and self.__compareValueLess <= inputV else False
        """
        if(self.__compareValueLess is not None and self.__compareValueGreater is not None):
            if(self.__compareValueLess < self.__compareValueGreater):
                return True if self.__compareValueGreater >= inputV and self.__compareValueLess <= inputV else False
            else:
                raise LogicException("The lower limit for \"in_range\" is larger or equal to the upper limit")

    def custom_logic(self, inputV):
        """
        Return True if the input value fulfills the logic set by the user.

        :param inputV: The value that will be compared to the condiations set in set_custom_logic
        :return: False if inputV in self.__notEqualValue, True if inputV in self.__EqualValue and True if self.__compareValueGreater < inputV < self.__compareValueLess else False
        """
        if inputV in self.__notEqualValue:
            return False
        elif inputV in self.__EqualValue:
            return True
        elif self.__compareValueGreater is not None and self.__compareValueLess is not None:
            return True if self.__compareValueGreater < inputV < self.__compareValueLess else False

    def _get_check_string(self, input):
        """
        Fetches check_string for input

        :param input:
        :return: self.__check_string(input)
        """
        return self.__check_string(input)
