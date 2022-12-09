from influxdb import InfluxDBClient

class Database:
    def __init__(self):
        self.client = None
        self.payload = []

    # Sets the FSM database
    def setDatabase(self, name, password, dbName):
        assert isinstance(name, str) and isinstance(password, str) and isinstance(dbName,str), "Input is not a String"
        self.client = InfluxDBClient('localhost', 8086, name, password, dbName)
        self.client.get_list_database()
        self.client.switch_database(dbName)
    def createDatabase(self, host, port,  name, password, dbName):
        assert isinstance(name, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        self.client = InfluxDBClient('localhost', 8086, name, password, dbName)
        self.client.create_database(dbName)
        self.client.get_list_database()
        self.client.switch_database(dbName)
    def update(self, data):
        assert isinstance(data, dict), "invalid data"

        return True

