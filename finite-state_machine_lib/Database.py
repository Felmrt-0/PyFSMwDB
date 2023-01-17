import time

from influxdb import InfluxDBClient
from columnar import columnar

class Database:
    def __init__(self):
        self.__client = None
        self.__payload = {}
        self.__columns = None

    # Sets the FSM database
    def setDatabase(self, name, password, dbName):
        assert isinstance(name, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        if self.__client is not None:
            self.__client.close()
        self.__client = InfluxDBClient('localhost', 8086, name, password, dbName)
        #self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def createDatabase(self, host='localhost', port=8086, username='root', password='root', dbName="DefaultDatabase"):
        assert isinstance(host, str), "Input is not a String"
        assert isinstance(port, int), "The port number has to be an integer"
        assert isinstance(username, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        if self.__client is not None:
            self.__client.close()
        self.__client = InfluxDBClient(host, port, username, password, dbName)
        self.__client.create_database(dbName)
        #self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def insert(self, data):
        if isinstance(data, list):
            self.__client.write_points(data)
        elif isinstance(data, dict):
            self.__client.write_points([data])
        else:
            return False    #borde kanske vara en exception
        return True

    def update(self, values:list):
        assert len(values) == len(self.__columns), "Size of values do not match size of stored columns"
        data = self.__payload
        data["time"] = datetime.datetime.now()
        data["fields"] = {}
        for i, c in enumerate(self.__columns):
            data["fields"][c] = values[i]
        self.__client.write_points([data])

    def delete(self, table, col, value):
        res = self.__client.query("SELECT " + str(col) + " FROM " + str(table) + " WHERE " + str(col) + "='" + str(value) + "';")
        if len(res.raw["series"]) == 0:
            return
        columns = res.raw["series"][0]["columns"]
        for i, t in enumerate(columns):
            if t == "time":
                time_pos=i
                break
        print(res.raw["series"][0]["values"])
        time = []
        for i in res.raw["series"][0]["values"]:
            time.append(i[time_pos])
        #time = res.raw["series"][0]["values"][0][time_pos]
        print("time", time)
        #self.__client.query("DELETE FROM " + str(table) + " WHERE time ='" + time + "';")
        for t in time:
            self.__client.query("DELETE FROM " + str(table) + " WHERE time ='" + t + "';")

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

    @staticmethod
    def print_formatter(headers, data):
        list_of_rows = []
        for d in data:
            list_of_elements=[]
            for d2 in d:
                if d2 is not None:
                    list_of_elements.append(d2)
                else:
                    list_of_elements.append("")
            list_of_rows.append(list_of_elements)
        return columnar(data=list_of_rows, headers=headers, justify="c", min_column_width=10)

    def print_latest_rows(self, table : str, number_of_rows=1):
        headers, data = self.get_latest_rows(table=table, number_of_rows=number_of_rows)
        return self.print_formatter(headers, data)

    def print_first_rows(self, table : str, number_of_rows=1):
        headers, data = self.get_first_rows(table=table, number_of_rows=number_of_rows)
        return self.print_formatter(headers, data)

    def print_everything(self, table : str):
        headers, data = self.get_everything(table)
        return self.print_formatter(headers, data)

    def custom_query(self, query : str):
        res = self.__client.query(query)
        try:
            res = res.raw['series'][0]
            return res["columns"], res["values"]  # (headers, data)
        except (KeyError, IndexError):
            return

    def set_payload(self, table, columns, tags:dict=None):
        self.__columns = columns

        if tags is not None:
            self.__payload = {
                "measurement" : table,
                "time" : datetime.datetime.now(),
                "tags" : tags
            }
        else:
            self.__payload = {
                "measurement": table,
                "time": datetime.datetime.now()
            }

    def payload_set_tags(self, tags: dict):
        self.__payload["tags"] = tags

    def payload_add_tags(self, tags: dict):
        if "tags" in self.__payload:
            self.__payload["tags"].update(tags)
        else:
            self.__payload["tags"] = tags

    def __del__(self):
        self.__client.close()

def payload_test():
    table = "PayloadTable"
    db = Database()
    db.setDatabase("root", "root", "DefaultDatabase")
    db.set_payload(table, ["Col1", "Col2"], tags={"Tag" : "TestTag4"})
    db.update(["Nr1", "Nr2"])
    print(db.print_everything(table))
    time.sleep(5)
    db.payload_set_tags({"Tag2" : "TestTag4"})
    db.update(["nr1", "nr2"])
    print(db.print_everything(table))
    del db

# for testing:
if __name__ == "__main__":
    import datetime

    payload_test()

    """col1 = 1
    col2 = 2

    data = {
        "measurement" : "TestTable",
        "tags": {
            "Info": "Test"
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
    #db.insert(data)
    #db.delete("TestTable", "locked", "bla")
    print(db.print_latest_rows("TestTable", 5))
    #print(db.print_everything("TestTable"))
    #print(db.custom_query("SELECT Col2 FROM TestTable WHERE Col2 = 2;"))
    print(db.custom_query("DELETE FROM TestTable WHERE time = 1;"))
    """
    # PAYLOAD RELATED THINGS ARE UNTESTED


