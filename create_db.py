import sqlite3

db_name = 'series.db'

def db_wrapper(func):
    def wrap():
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        func(cursor)
        connection.close()
    return wrap

@db_wrapper
def create_db(cursor):
    cursor.execute("Drop table if exists measurements")
    cursor.execute("Create table measurements(sensor_id, timestamp, temperature, conductivity)")

    result = cursor.execute("SELECT * FROM sqlite_master")
    print(result.fetchall())

if __name__ == "__main__":
    create_db()