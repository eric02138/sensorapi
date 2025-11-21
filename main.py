from flask import Flask
from flask_restx import Api, Namespace, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine


app = Flask(__name__)
api = Api(app, 
          version='1.0', 
          title='Sensor API', 
        #   doc='/doc',
          description='A minimal backend that ingests sensor data ')

"""
Using SQLite to store measurement records because there's no installation required.
A NoSQL db could actually be more responsive, but I want to cut down on environment 
overhead.
Using SQLAlchemy here for ease of connecting the app to the db.  But I'll be using 
raw sql queries to underscore that each function maps directly to a query, without
the obfuscation of an ORM.
"""
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///measurements.db"

# db = SQLAlchemy()
# db.init_app(app)

db_url = "sqlite:///measurements.db"
engine = create_engine(db_url)

"""
Namespacing the application is good practice.  As the app grows,
there could be more url routes in different folders. These child routes could then 
be attached to the parent at this level.
"""
app_info_ns = Namespace('app_info', 
                        description='Information about this application')
api.add_namespace(app_info_ns, '/app_info')

measurements_ns = Namespace('measuresments', 
                            description="Namespace for measurement data")
api.add_namespace(measurements_ns, '/measurements')

@app_info_ns.route('/')
class AppInfo(Resource):
    def get(self):
        return {
            'app_name': 'sensor api',
            'version': '1.0',
            'owner': 'emattison',
            'docs_url': '/'
            }

measurement = api.model('Measurement', 
    {
        'sensor_id': fields.String(required=True, 
                                   description="Unique sensor id"),
        'timestamp': fields.DateTime(required=True, 
                                    description="Created datetime for data in classic ISO format",
                                    dt_format="%Y-%m-%dT%H:%M:%S.%fZ"),
        'temperature': fields.Integer(required=True, 
                                      description="Celsius temperature reading"),
        'conductivity': fields.Integer(required=True, 
                                       description="Conductivity in microsiemens/cm")
    }
)

@measurements_ns.route('/')
class Measurements(Resource):

    def get(self):
        with engine.connect() as connection:
            sql = """select * from measurements"""
            result = connection.execute(text(sql))
            for row in result:
                print(row)
        return
    
    #@measurements_ns.expect(measurement) # data validation
    #@measurements_ns.marshall_with(measurement)
    def post(self):
        with engine.connect() as connection:
            print(api.payload)
            measurement_data = api.payload
            sql = """Insert into measurements (sensor_id, timestamp, temperature, conductivity) 
                    values (:sensor_id, :timestamp, :temperature, :conductivity)"""
            params = {'sensor_id': measurement_data['sensor_id'],
                    'timestamp': measurement_data['timestamp'],
                    'temperature': measurement_data['temperature'],
                    'conductivity': measurement_data['conductivity']}
            connection.execute(text(sql), params)
            connection.commit()
        return

if __name__ == '__main__':
    app.run(debug=True)