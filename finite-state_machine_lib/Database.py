from influxdb import InfluxDBClient

class Database:
    def __init__(self):
        self.__client = None
        self.__payload = []

    # Sets the FSM database
    def setDatabase(self, name, password, dbName):
        assert isinstance(name, str) and isinstance(password, str) and isinstance(dbName,str), "Input is not a String"
        self.__client = InfluxDBClient('localhost', 8086, name, password, dbName)
        self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def createDatabase(self, host='localhost', port=8086, username='root', password='root', dbName="DefaultDatabase"):
        assert isinstance(host, str), "Input is not a String"
        assert isinstance(port, int), "The port number has to be an integer"
        assert isinstance(username, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        self.__client = InfluxDBClient(host, port, username, password, dbName)
        self.__client.create_database(dbName)
        self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def update(self, data):
        if isinstance(data, list):
            self.__client.write_points(data)
        elif isinstance(data, dict):
            self.__client.write_points([data])
        else:
            return False
        return True

    # doesn't really work yet
    def get_everything(self, table):
        res = self.__client.query("SELECT * FROM " + table + ";")
        print(res.raw)
        res = res.raw['series']
        for i in res:
            for j in i.items():
                if isinstance(j[1], list):
                    for k in j[1]:
                        print(k)

# for testing:
if __name__ == "__main__":
    import datetime

    col1 = 1
    col2 = 2

    data = {
        "measurement" : "TestTable",
        "tags" : {
            "Info" : "Test"
        },
        "time" : datetime.datetime.now(),
        "fields" : {
            "Col1" : col1,
            "Col2" : col2
        }
    }
    data = [data]

    db = Database()
    db.createDatabase()
    #db.update(data)
    db.get_everything("TestTable")




