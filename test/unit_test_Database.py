from finite_state_machine_lib.Database import Database
import datetime

def database_test2():
    table = "PayloadTable"
    db = Database()
    # set database test
    try:
        db.set_database("root", "root", "mydb")
        set_database_test = True
    except Exception:
        print("set_database_test Failed")
        set_database_test = False


    # set payload test
    try:
        db.set_payload(table, ["Col1", "Col2"], tags={"Tag" : "TestTag3"})
        set_payload_test = True
    except Exception:
        print("set_payload_test Failed")
        set_payload_test = False


    # update test
    try:
        db.update(["Nr1", "Nr2"])
        update_test = True
    except Exception:
        print("update_test Failed")
        update_test = False


    #print_everything test
    try:
        print(db.print_everything(table))
        print_everything_test = True
    except Exception:
        print("print_everything_test Failed")
        print_everything_test = False


    # payload_set_tags test
    try:
        db.payload_set_tags({"Tag2" : "TestTag4"})
        set_payload_tags_test = True
    except Exception:
        print("set_payload_tags_test Failed")
        set_payload_tags_test = False


    return set_database_test, update_test, set_payload_test, set_payload_tags_test, print_everything_test

def database_test1():
    custom_query_test = None

    database = Database()
    table = "test"
    tag = "tag"
    data = {
        "measurement" : table,
                "tags": {
                    tag : "cool test"
                         },
                "time" : datetime.datetime.now(),
                "fields" : {
                    "is cool" : "yes"
                }
    }
    try:
        database.create_database(dbName="mydb")
        database.create_database()
        create_database_test = True
    except Exception:
        print("create_database_Test Failed")
        create_database_test = False

    try:
        database.insert([data])
        insert_test = True
    except Exception:
        print("insert_Test Failed")
        insert_test = False

    try:
        first_row = database.get_first_rows(table)
        if first_row[0] == ['time','is cool', 'tag'] and first_row[1][0][1] == 'yes' and first_row[1][0][2] == 'cool test':
            get_first_rows_test = True
        else:
            print("get_first_rows_test Failed")
            get_first_rows_test = False
    except Exception:
       print("get_first_rows_test Failed")
       get_first_rows_test = False

    try:
        print(database.print_first_rows(table))
        print_first_rows_test = True
    except Exception:
        print("print_first_rows_test Failed")
        print_first_rows_test = False



    try:
        database.delete(table, tag, 'yes')
        delete_test = True
    except Exception:
        print("delete_Test Failed")
        delete_test = False

    database.insert(data)

    try:
        last_row = database.get_latest_rows(table)
        if last_row[0] == ['time', 'is cool', 'tag'] and last_row[1][0][1] == 'yes' and last_row[1][0][2] == 'cool test':
            get_latest_rows_test = True
        else:
            print("get_last_rows_test Failed")
            get_latest_rows_test = False
    except Exception:
        print("get_last_rows_test Failed")
        get_latest_rows_test = False


    try:
        print(database.print_latest_rows(table))
        print_latest_rows_test = True
    except Exception:
        print("print_latest_rows_test Failed")
        print_latest_rows_test = False


    try:
        database.get_everything(table)
        get_everything_test = True
    except Exception:
        print("get_everything_Test Failed")
        get_everything_test = False

    try:
        newtag = {
            "test tag" : "this is a test tag"
        }
        database.payload_set_tags(newtag)
        if database.getPayload()["tags"] == newtag:
            payload_set_tags_test = True
        else:
            print("payload_set_tags_test Failed")
            payload_set_tags_test = False
    except Exception:
        print("payload_set_tags_test Failed")
        payload_set_tags_test = False


    try:
        newtag1 = {
            "test tag": "taggers",
            "super tag": "super"
        }
        database.payload_add_tags(newtag1)
        if database.getPayload()["tags"] == newtag1:
            payload_add_tags_test = True
        else:
            print("payload_set_tags_test Failed")
            payload_add_tags_test = False
    except Exception:
        print("payload_set_tags_test Failed")
        payload_add_tags_test = False

    database.custom_query("DROP SERIES FROM /.*/")
    try:
        database.get_everything(table)
        print("custom_query_test Failed")
        custom_query_test = False
    except Exception:
        custom_query_test = True


    database.close_database()
    try:
        database.insert(data)
        print("close_Test Failed")
        close_database_test = False
    except Exception:
        close_database_test = True


    return payload_add_tags_test, payload_set_tags_test ,custom_query_test, create_database_test, insert_test, get_first_rows_test, delete_test, get_latest_rows_test, get_everything_test, close_database_test, print_latest_rows_test, print_first_rows_test

if __name__ == "__main__":
    test1 = database_test1()
    test2 = database_test2()
