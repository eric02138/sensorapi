import sqlite3

connection = sqlite3.connect("series.db")
cursor = connection.cursor()
cursor.execute("Drop table if exists measurements")
cursor.execute("Create table measurements(sensor_id, timestamp, temperature, conductivity)")
result = cursor.execute("SELECT name FROM sqlite_master")
print(result.fetchall())
connection.close()