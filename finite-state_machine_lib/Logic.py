import math
class Logic:
    def __init__(self, gt=-math.inf, lt=math.inf, default=False):
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
        self.__less_than = lt if lt is not None else math.inf
