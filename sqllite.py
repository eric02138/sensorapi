import sqlite3
import random
from datetime import datetime

SENSORS = ['sensor_001', 'sensor_002', 'sensor_003']
# Realistic value ranges for water quality monitoring
TEMP_RANGE = (20.0, 30.0) # Celsius
CONDUCTIVITY_RANGE = (1000, 3000) # microsiemens/cm

db_name = 'series.db'

def db_wrapper(func):
    def wrap():
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        func(cursor)
        connection.close()
    return wrap

@db_wrapper
def do_db_stuff(cursor):
    # connection = sqlite3.connect("series.db")
    # cursor = connection.cursor()
    cursor.execute("Drop table if exists measurements")
    cursor.execute("Create table measurements(sensor_id, timestamp, temperature, conductivity)")

    sensor_id = SENSORS[0]
    timestamp = datetime.utcnow().isoformat() + 'Z'
    temperature = round(random.uniform(*TEMP_RANGE), 1)
    conductivity = random.randint(*CONDUCTIVITY_RANGE)
    sql_string = f"""Insert into measurements values (
                '{sensor_id}', 
                '{timestamp}', 
                {temperature}, 
                {conductivity}
                )"""
    cursor.execute(sql_string)

    sensor_id = SENSORS[1]
    timestamp = datetime.utcnow().isoformat() + 'Z'
    temperature = round(random.uniform(*TEMP_RANGE), 1)
    conductivity = random.randint(*CONDUCTIVITY_RANGE)
    sql_string = f"""Insert into measurements values (
                '{sensor_id}', 
                '{timestamp}', 
                {temperature}, 
                {conductivity}
                )"""
    cursor.execute(sql_string)

    sensor_id = SENSORS[2]
    timestamp = datetime.utcnow().isoformat() + 'Z'
    temperature = round(random.uniform(*TEMP_RANGE), 1)
    conductivity = random.randint(*CONDUCTIVITY_RANGE)
    sql_string = f"""Insert into measurements values (
                '{sensor_id}', 
                '{timestamp}', 
                {temperature}, 
                {conductivity}
                )"""
    cursor.execute(sql_string)


    result = cursor.execute("SELECT * FROM measurements")
    print(result.fetchall())
    # connection.close()

if __name__ == "__main__":
    do_db_stuff()