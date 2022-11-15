
class Handler:

    # it should take functions or objects as arguments
    def __init__(self, approachP, dig, approachT1, approachLR, dump, approachT2, done=None):
        print("#" * 20 + "\nINITIALIZING HANDLER\n" + "#" * 20)

        if not (callable(approachP) and callable(dig) and callable(approachT1) and callable(approachLR) and
                callable(dump) and callable(approachT2)):
            raise TypeError
        if done is not None and not callable(done):
            raise TypeError

        self.__approachPit = approachP
        self.__digFromPile = dig
        self.__approachTurningPoint = approachT1
        self.__approachLoadReceiver = approachLR
        self.__dumpOnLoadReceiver = dump
        self.__approachTurningPoint2 = approachT2
        self.__done = done if done is not None else False

        # fix permissions later
        self.__sap_a_1 = open("SAP.A.1", "r")
        self.__cvs_1 = open("CVS.1", "r")
        self.__ls_1 = open("LS.1", "r")
        self.__tvds_1 = open("TVDS.1", "r")
        self.__stp_a = open("STP.A", "r")

    def run(self):
        while True:
            self.__approachPit(self.__sap_a_1, self.__cvs_1, self.__ls_1, self.__tvds_1, self.__stp_a)
            self.__digFromPile(self.__sap_a_1, self.__cvs_1, self.__ls_1, self.__tvds_1)
            self.__approachTurningPoint(self.__cvs_1, self.__ls_1, self.__tvds_1)
            self.__approachLoadReceiver(self.__cvs_1, self.__ls_1, self.__tvds_1)
            self.__dumpOnLoadReceiver(self.__cvs_1, self.__ls_1, self.__tvds_1)
            self.__approachTurningPoint2(self.__cvs_1, self.__ls_1, self.__tvds_1)
            if self.__done():
                break
        print("run() is exiting")

    def __del__(self):
        print("#"*20+"\nDELETING THE HANDLER\n"+"#"*20)
        self.__sap_a_1.close()
        self.__cvs_1.close()
        self.__ls_1.close()
        self.__tvds_1.close()
        self.__stp_a.close()


# for testing
if __name__ == "__main__":
    pass
