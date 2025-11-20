from flask import Flask
from flask_restx import Api, Namespace, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
api = Api(app, 
          version='1.0', 
          title='Sensor API', 
        #   doc='/doc',
          description='A minimal backend that ingests sensor data ')

"""
Using SQLite to store measurement records because there's no installation required.
I'll be using regular SQL for the queries (not sqlalchemy's object notation)
to demonstrate that this could be any RDBS.  A NoSQL db could actually be more responsive,
but I want to cut down on environment overhead.
"""
db = SQLAlchemy()
db_name = 'series.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

"""
Namespacing the application is good practice.  As the app grows,
there could be more url routes in different folders. These child routes could then 
be attached to the parent at this level.
"""
app_info_ns = Namespace('app_info', description='Information about this application')
api.add_namespace(app_info_ns, '/app_info')

measurements_ns = Namespace('measuresments', description="Namespace for measurement data")
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

@measurements_ns.route('/')
class Measurements(Resource):
    def get(self):
        return {
            'measurements': [1, 2, 3]
        }
    
    def post(self):
        return

if __name__ == '__main__':
    app.run(debug=True)