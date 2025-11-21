import random
from datetime import datetime
from sqlalchemy import create_engine, text

SENSORS = ['sensor_001', 'sensor_002', 'sensor_003']
# Realistic value ranges for water quality monitoring
TEMP_RANGE = (20.0, 30.0) # Celsius
CONDUCTIVITY_RANGE = (1000, 3000) # microsiemens/cm

db_url = "sqlite:///measurements.db"
engine = create_engine(db_url, echo=True)

def do_db_stuff():
    with engine.connect() as connection:
        # connection.execute(text("Drop table if exists measurements"))
        # connection.execute(text("Create table measurements(" \
        #                         "sensor_id, timestamp, temperature, conductivity)"))

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
        connection.execute(text(sql_string))


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
        connection.execute(text(sql_string))

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
        connection.execute(text(sql_string))

        result = connection.execute(text("SELECT * FROM measurements"))
        connection.commit()
        print(result.fetchall())

if __name__ == "__main__":
    do_db_stuff()