from sqlalchemy import create_engine, text

db_url = "sqlite:///measurements.db"
engine = create_engine(db_url, echo=True)

def create_db():
    with engine.connect() as connection:
        connection.execute(text("Drop table if exists measurements"))
        connection.execute(text("Create table measurements(sensor_id, timestamp, temperature, conductivity)"))
        connection.commit()
        result = connection.execute(text("SELECT * FROM sqlite_master"))
        print(result.fetchall())

if __name__ == "__main__":
    create_db()