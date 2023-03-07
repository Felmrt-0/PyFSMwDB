import time
import datetime
from influxdb import InfluxDBClient
from columnar import columnar

from finite_state_machine_lib.CustomExceptions import DatabaseTableEmpty


class Database:
    """
    A database class that contains a database and payload

    Attributes
    ----------
    client : database
        The Database client the object is using

    payload : dict
        Payload to add to database

    columns : int
        Number of columns the table in database has??

    Methods
    -------
    set_database(self, name:str, password:str, dbName:str)
        Connects to a database

    create_database(self, name:str, password:str, dbName:str)
        Creates an Influx 2.0 database

    close_database()
        Closes database

    insert(data)
        Inserts data into database

    update(values:list)
        Updates a table

    delete(table, col, value)
        Removes value from a specific column of table

    get_latest_rows(table, rows)
        Fetches the latest number of rows  of table

    get_first_rows(table, rows)
        Fetches the first number of rows of table

    get_everything(table)
        Fetches entire Table

    print_formatter()

    print_latest_rows(table : str, rows)
        Prints the latest number of rows  of table in the terminal

    print_first_rows(table : str, rows)
        Prints the first number of rows  of table in the terminal

    print_everything(table : str)
        Prints entire table into terminal

    custom_query(query : str)
        Querys database with custom command

    set_payload(table, columns, tags:dict=None)
        Sets the payload structure

    payload_set_tags(tags: dict)
        Sets payload tag

    payload_add_tags(tags: dict)
        Adds a tag to the payload


    """
    def __init__(self):
        self.__client = None
        self.__payload = {}
        self.__columns = None

    # Sets the FSM database
    def set_database(self, name:str, password:str, dbName:str):
        """
        Sets an exsiting Influx 2.0 database to be utilized

        :param name: The name of the user
        :param password: The password of the user
        :param dbName: The name of the desired database
        :return: None
        """
        assert isinstance(name, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        if self.__client is not None:
            self.__client.close()
        self.__client = InfluxDBClient('localhost', 8086, name, password, dbName)
        #self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def create_database(self, host='localhost', port=8086, username='root', password='root', dbName="DefaultDatabase"):
        """
        Logs in as a client and creates a new InfluxDB database and sets it as client for the database object.
        If a database is already open it's closed first.

        :param host:
        :param port: The network port that the database will use
        :param username: The name of the user
        :param password: The password of the user
        :param dbName: The name of the desired database
        :return: None
        """

        assert isinstance(host, str), "Input is not a String"
        assert isinstance(port, int), "The port number has to be an integer"
        assert isinstance(username, str) and isinstance(password, str) and isinstance(dbName, str), "Input is not a String"
        if self.__client is not None:
            self.__client.close()
        self.__client = InfluxDBClient(host, port, username, password, dbName)
        self.__client.create_database(dbName)
        #self.__client.get_list_database()
        self.__client.switch_database(dbName)

    def close_database(self):
        """
        Closes the open database.

        :return: None
        """
        self.__client.close()

    def insert(self, data):
        """
        Inserts a list or dictanary as data into the database

        :param data: The data that will be inserted into the database
        :return: True
        """
        assert isinstance(data, list) or isinstance(data, dict), "Data should be a list or a dictunary"
        if isinstance(data, list):
            self.__client.write_points(data)
        elif isinstance(data, dict):
            self.__client.write_points([data])
        else:
            return False    #borde kanske vara en exception
        return True

    def update(self, values:list):
        """
        Updates the table with new values depending on the instance variables: payload and columns

        :param values: The value to be entered into the column.
        :return: None
        """
        assert len(values) == len(self.__columns), "Size of values do not match size of stored columns"
        data = self.__payload
        data["time"] = datetime.datetime.now()
        data["fields"] = {}
        for i, c in enumerate(self.__columns):
            data["fields"][c] = values[i]
        self.__client.write_points([data])

    def delete(self, table, col, value):
        """
        Deletes the values from the seleted table where col == value.

        :param table: The table to delete from
        :param col: The name of the column
        :param value: The value the columns might contain
        :return: None
        """
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
        """
        gets the last number of row from a table

        :param table:
        :param number_of_rows:
        :return:
        """
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        try:
            res = res.raw["series"][0]
            data = res["values"][::-1]
            headers = res["columns"]
            return headers, data
        except IndexError:
            raise DatabaseTableEmpty()

    def get_first_rows(self, table : str, number_of_rows=1):
        """
        gets the first number of rows from table
        :param table:
        :param number_of_rows:
        :return:
        """
        res = self.__client.query("SELECT * FROM " + table + " ORDER BY DESC LIMIT " + str(number_of_rows) + ";")
        try:
            res = res.raw["series"][0]
            data = res["values"][::-1]
            headers = res["columns"]
            return headers, data
        except IndexError:
            raise DatabaseTableEmpty()

    def get_everything(self, table : str):
        """
        fetches entire table

        :param table:
        :return:
        """
        res = self.__client.query("SELECT * FROM " + table + ";")
        try:
            res = res.raw['series'][0]
            headers = res["columns"]
            data = res["values"]
            return headers, data
        except IndexError:
            raise DatabaseTableEmpty()

    @staticmethod
    def print_formatter(headers, data):
        """
        Formats the output in terminal

        :param headers:
        :param data:
        :return:
        """
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
        """
        prints the latest number of rows of table into the terminal

        :param table:
        :param number_of_rows:
        :return:
        """
        headers, data = self.get_latest_rows(table=table, number_of_rows=number_of_rows)
        return self.print_formatter(headers, data)

    def print_first_rows(self, table : str, number_of_rows=1):
        """
        prints first number of rows from table into the terminal

        :param table:
        :param number_of_rows:
        :return:
        """
        headers, data = self.get_first_rows(table=table, number_of_rows=number_of_rows)
        return self.print_formatter(headers, data)

    def print_everything(self, table : str):
        """
        prints entire table into terminal

        :param table:
        :return:
        """
        headers, data = self.get_everything(table)
        return self.print_formatter(headers, data)

    def custom_query(self, query : str):
        """
        Querys the database with the given command

        :param query:
        :return:
        """
        res = self.__client.query(query)
        try:
            res = res.raw['series'][0]
            return res["columns"], res["values"]  # (headers, data)
        except (KeyError, IndexError):
            return

    def set_payload(self, table, columns, tags:dict=None):
        """
        sets the payload structure

        :param table:
        :param columns:
        :param tags:
        :return:
        """
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
        """
        sets payload tag

        :param tags:
        :return:
        """
        self.__payload["tags"] = tags

    def getClient(self):
        """
        gets objects client

        :return self.__client:
        """
        return self.__client

    def getPayload(self):
        """
        gets objects Payload

        :return: self.__payload
        """
        return self.__payload
    def payload_add_tags(self, tags: dict):
        """
        adds a payload tag

        :param tags:
        :return:
        """
        if "tags" in self.__payload:
            self.__payload["tags"].update(tags)
        else:
            self.__payload["tags"] = tags

    def __del__(self):
        """

        :return:
        """
        if self.__client is not None:
            self.__client.close()

# test function
def payload_test():
    table = "PayloadTable"
    db = Database()
    db.set_database("", "", "mydb")
    db.set_payload(table, ["Col1", "Col2"], tags={"Tag" : "TestTag4"})
    db.update(["Nr1", "Nr2"])
    print(db.print_first_rows(table))
    time.sleep(5)
    db.payload_set_tags({"Tag2" : "TestTag4"})
    db.update(["nr1", "nr2"])
    print(db.print_latest_rows(table))

def exception_test():
    db = Database()
    db.create_database()
    table = "BabyDriverTest"
    rows = db.get_latest_rows(table, 1)
    print(rows)


# for testing:
if __name__ == "__main__":


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


