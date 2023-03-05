from finite_state_machine_lib.Database import Database
def createDatabase_test():
    database = Database()
    database.create_database(dbName="testdatabase")
    if checkDatabase(database) :
        return True
    return False

def checkDatabase(database):
    assert isinstance(database, Database), "not a database"
    return database.getClient()