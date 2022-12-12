from influxdb import InfluxDBClient
from columnar import columnar

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

    def delete(self, table, col, value):
        self.__client.query("DELETE FROM "+ str(table) + " WHERE " + str(col) + " = " + str(value))

    def get_latest_rows(self, table : str, number_of_rows=1):
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        res = res.raw["series"][0]
        data = res["values"][::-1]
        headers = res["columns"]
        return headers, data

    def get_first_rows(self, table : str, number_of_rows=1):
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        res = res.raw["series"][0]
        data = res["values"][::-1]
        headers = res["columns"]
        return headers, data

    def get_everything(self, table : str):
        res = self.__client.query("SELECT * FROM " + table + ";")
        res = res.raw['series'][0]
        headers = res["columns"]
        data = res["values"]
        return headers, data

    def print_formatter(self, headers, data):
        return columnar(data=data, headers=headers, justify="c", min_column_width=10)

    def print_latest_rows(self, table : str, number_of_rows=3):
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        res = res.raw["series"][0]
        data = res["values"][::-1]
        headers = res["columns"]
        return self.print_formatter(headers, data)

    def print_first_rows(self, table : str, number_of_rows=1):
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        res = res.raw["series"][0]
        data = res["values"][::-1]
        headers = res["columns"]
        return self.print_formatter(headers, data)

    def print_everything(self, table : str):
        res = self.__client.query("SELECT * FROM " + table + ";")
        res = res.raw['series'][0]
        headers = res["columns"]
        data = res["values"]
        return self.print_formatter(headers, data)

    def custom_query(self, query : str):
        if not isinstance(query, str):
            query = str(query)
        res = self.__client.query(query);
        res = res.raw['series'][0]
        return res["columns"], res["values"]




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
    db.setDatabase("root", "root", "DefaultDatabase")
    #db.createDatabase()
    #db.update(data)
    #print(db.print_everything("TestTable"))
    #print(db.get_latest_rows("TestTable"))




