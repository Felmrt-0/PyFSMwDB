
class TransitionNotFoundException(Exception):
    """
    Thrown when a State couldn't find a transition with the input given
    """
    def __init__(self, condition, connections, message="Couldn't find condition in connections"):
        self.condition = condition
        self.connections = connections
        self.message = message + "\nCondition: " + str(self.condition) + "\nConnections" + str(self.connections)
        super().__init__(self.message)


class LogicException(Exception):
    """
    Thrown for general error in Logic
    """
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)


class CustomLogicException(Exception):
    """
    Thrown if an exception relating to custom logic occurs
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseTableEmpty(Exception):
    """
    Thrown if database query returned nothing
    """
    def __init__(self, message="The query returned nothing"):
        self.message = message
        super().__init__(self.message)


if __name__ == "__main__":
    #raise TransitionNotFoundException(condition=2, connections={"ne": 2})
    raise LogicException("The lower limit for \"in_range\" is larger or equal to the upper limit")
    #raise CustomLogicException("hej")