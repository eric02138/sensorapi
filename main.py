import json
from datetime import datetime, timedelta, UTC
from flask import Flask
from flask_restx import Api, Namespace, Resource, fields, reqparse
from sqlalchemy import text, create_engine

SENSORS = ['sensor_001', 'sensor_002', 'sensor_003']

"""
Realistic value ranges for water quality monitoring.
Leaving these here because these values could be used to notify data 
scientists if sensors are returning bad data.  Not in scope, but maybe if I 
have the time... ha ha.  Right.
"""
TEMP_RANGE = (20.0, 30.0) # Celsius
CONDUCTIVITY_RANGE = (1000, 3000) # microsiemens/cm
DATA_GRANULARITY = [60, 5] # Default should be hour increments, detailed should be 5 minutes
GRANULARITY_THRESHOLD = 1 # Default threshhold between change in granularity should be 1 hour


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
Using SQLAlchemy's engine for connecting the app to the db.  But I'll be using 
raw sql queries to underscore that each function maps directly to a query, without
the obfuscation of an ORM.  Oddly, Flask makes doing this seemingly simple connection 
surprisingly difficult.  
"""
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///measurements.db"

# db = SQLAlchemy()
# db.init_app(app)

db_url = "sqlite:///measurements.db"
engine = create_engine(db_url)

dt_parser = reqparse.RequestParser()
dt_parser.add_argument('start_dt',
                       type=datetime.fromisoformat,
                       required=False,
                       help="Start datetime to aggregate from in ISO 8601 format "
                       "(e.g., 2025-11-21T10:00:00)")
dt_parser.add_argument('end_dt',
                       type=datetime.fromisoformat,
                       required=False,
                       help="End datetime to aggregate from in ISO 8601 format "
                       "(e.g., 2025-11-21T11:00:00)")


"""
Namespacing the application is good practice.  As the app grows,
there could be more url routes in different folders. These child routes could then 
be attached to the parent at this level.
"""
ns = Namespace('measuresments', 
                            description="Namespace for measurement data")
api.add_namespace(ns, '/measurements')

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

"""
For now, the default route is used for populating the database through the post
method and getting a list of sensors using the get method, mostly because I think 
the get method should always return some kind of meaningful data.  So the url 
"/measurements" might be replaced by "/sensors" in the future...
returns:
    - json serialized list of sensor_ids
"""
@ns.route('/')
class Measurements(Resource):
    """
    Default route - just get the sensor ids
    """
    def get(self):
        with engine.connect() as connection:
            sql = """select distinct(sensor_id) from measurements"""
            result = connection.execute(text(sql))
            sensor_id_list = [r for (r,) in result] # convert output from tuples
            result = {'sensor_ids': sensor_id_list, 'count': len(sensor_id_list)}
        return json.dumps(result)
    
    """
    Post method used by the sensor_simulator.py script
    params: 
        - a measurement object
    returns: 
        - None
    """
    @ns.expect(measurement) # very basic data injest validation
    def post(self):
        with engine.connect() as connection:
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
    
"""
Returns measurement data for a specified sensor.
params:
    - sensor_id: required
    - start_dt: optional, default to current time
    - end_dt: optional, default to 1 hour from start_dt
returns:
    - json serialized list of aggregated measurement objects
"""
@ns.route('/<sensor_id>')
class SensorMeasurements(Resource):
    """
    Get Measurements by sensor (and filter by query parameters)
    params:
        - sensor_id: required
        - start_dt: optional, defaults to one hour ago
        - end_dt: optional, defaults to one hour after start_dt
    returns:
        - a json-serialized 
    """
    def get(self, sensor_id):
        with engine.connect() as connection:

            args = dt_parser.parse_args()
            start_dt_query_param = args.get("start_dt")
            end_dt_query_param = args.get("end_dt")

            if not start_dt_query_param and not end_dt_query_param:
                #default to the last hour                
                end_dt = datetime.now(UTC)
                start_dt = end_dt - timedelta(hours=GRANULARITY_THRESHOLD)

            if start_dt_query_param: 
                start_dt = datetime.strptime(start_dt_query_param)
                end_dt = start_dt + timedelta(hours=GRANULARITY_THRESHOLD)
            if end_dt_query_param:
                end_dt = datetime.strptime(end_dt_query_param)
                if not start_dt_query_param:  # assume the user wants the previous hour
                    start_dt = end_dt - timedelta(hours=GRANULARITY_THRESHOLD)  

            """
            if the end datetime is within the last hour, assume the user wants to see 5 minute
            intervals.  Otherwise, assume they want to see 60 minute intervals.
            """ 
            data_granularity = DATA_GRANULARITY[0]
            if end_dt >= datetime.now(UTC) - timedelta(hours=GRANULARITY_THRESHOLD):
                data_granularity = DATA_GRANULARITY[1]

            start_dt = start_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            end_dt = end_dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            """
            Modified from Stackoverflow.  The integer division in this query essentially
            takes a numerical unix timestamp, divides it by the specified interval and then 
            reconstitutes the value, having lopped off the unwanted extra seconds.  Pretty 
            clever, I wish I had throught of it.
            """

            sql = """
                SELECT
                strftime('%Y-%m-%dT%H:%M:%S.%fZ', datetime((strftime('%s', timestamp) / (5 * 60)) * (5 * 60), 'unixepoch')) AS interval_start,
                MIN(temperature) AS min_temperature,
                MAX(temperature) AS max_temperature,
                AVG(temperature) AS average_temperature,
                MIN(conductivity) AS min_conductivity,
                MAX(conductivity) AS max_conductivity,
                AVG(conductivity) AS average_conductivity,
                COUNT(*) AS record_count
                FROM
                measurements
                WHERE sensor_id=:sensor_id 
                AND interval_start >= :start_dt
                AND interval_start < :end_dt
                GROUP BY
                interval_start
                ORDER BY
                interval_start desc;
            """

            # sql = f"""select * from measurements where sensor_id=:sensor_id
            #           order by timestamp desc"""
            params = {'sensor_id': sensor_id,
                      'start_dt': start_dt, 
                      'end_dt': end_dt,
                      'data_granularity': data_granularity}
            result = connection.execute(text(sql), params)
            measurements = []
            for row in result.fetchall():
                dd = {
                    'interval_start': row[0],
                    'min_temperature': row[1],
                    'min_temperature': row[2],
                    'min_temperature': row[3],
                    'min_conductivity': row[4],
                    'min_conductivity': row[5],
                    'min_conductivity': row[6],
                    'record_count': row[7]
                }
                measurements.append(dd)
            result = {'sensor_ids': [sensor_id], 
                      'measurements': measurements}
        return json.dumps(result)
    
if __name__ == '__main__':
    app.run(debug=True)