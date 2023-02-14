
class TransitionNotFoundException(Exception):
    """
    Thrown when a State couldn't find a transition with the input given
    """
    def __init__(self, condition, connections, message="Couldn't find condition in connections"):
        self.condition = condition
        self.connections = connections
        self.message = message
        super().__init__(self.message)




if __name__ == "__main__":
    raise TransitionNotFoundException(2, {"ne": 2})
