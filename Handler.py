class Handler:
    approachPit = None
    digFromPile = None
    approachTurningPoint = None
    approachLoadReceiver = None
    dumpOnLoadReceiver = None
    approachTurningPoint = None

    def __init__(self, approachP, dig, approachT1, approachLR, dump, approachT2):
        print("#" * 20 + "\nINITIALIZING HANDLER\n" + "#" * 20)
        self.approachPit = approachP
        self.digFromPile = dig
        self.approachTurningPoint = approachT1
        self.approachLoadReceiver = approachLR
        self.dumpOnLoadReceiver = dump
        self.approachTurningPoint = approachT2

    def __del__(self):
        # delete possible other things
        print("#"*20+"\nDELETING THE HANDLER\n"+"#"*20)


# for testing
if __name__ == "__main__":
    pass
