from config import DBConnection

if __name__ == "__main__":
    dbc: DBConnection = DBConnection()
    dbc.create_tables()
