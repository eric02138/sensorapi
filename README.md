# SensorAPI
A minimal Flask backend that ingests sensor data 

## Design Considerations
I wanted to make setting up this demo as simple as possible, with minimal dependencies.  This actually led to more than a few headaches, namely connecting to the database (Flask *really* wants you to use SQLAlchemy) and the limitations of SQLite3 (which doesn't have a native DateTime field).  Using a NoSQL database like MongoDB might allow for greater flexibility were the application to grow.

## Installation
Create a virtual environment with a recent-ish version of Python 3 - I'm using Python 3.12.7.  Pyenv is nifty, too.  
`>> pyenv virtualenv sensorapi`

Next, install the python packages we'll be using:  
`>> pip install -r requirements.txt`  
(This is old school - I like Poetry, but that's another install.)

Let's create the SQLite3 database:  
`>> python create_db.py`  
You should now see `measurements.db` in your working directory.

Run the application:  
`>> python main.py`  
In a browser go to [http://127.0.0.1:5000](http://127.0.0.1:5000).  You should see the Swagger UI documentation page.

## Adding and Retrieving Data
With the Flask application running, open a new terminal window and run the `sensor_simulator.py` script to add some data to the database.  (Make sure you've activated the virtual environment in the new window.)  
`>> python sensor_simulator.py`  
Press any key when you feel like you've added enough data.  For best results, leave this running for over an hour.  Grab yourself a coffee.  You've earned it.

Welcome back.  To retrieve your data, run  
`>> python requestor.py`  
This script has a few example requests to get you started.  You could also use Postman.

## Overview and Lessons Learned
As I mentioned, I erred on the side of simplicity (to my detriment, honestly).  Using SQLite3 for local development is fine for a proof of concept, if you had to deploy the code onto a service that used a "real" database, it could very well fail.  

Flask-RestX is a pretty nice API building package.  It provides you with a bunch of nice wrappers for namespacing and documenting your APIs.  For example, if this API had to be broken up into separate scripts in different folders, namespacing would become critical.  Interestingly, Flask-RestX is getting rid of their [request parser](https://flask-restx.readthedocs.io/en/latest/parsing.html) and encouraging users to use marshmallow instead.  Maybe marshmallow could replace Flask-RestX's somewhat clunky `api.model`?

Other than the `@ns.expect(measurement)` wrapper call, I'm not doing much data validation on the data ingest function, mainly because that wasn't part of the assignment.  But it would be good to use something like pydantic to check the values being posted.  Maybe the endpoint could enforce the temperature and conductivity ranges.  Then again, it would probably be useful to keep those readings and flag them as erroneous, letting operators know that their sensors are wonky.

Overall, this was a fun exercise that got me thinking about what I would like to see if I owned a couple of these devices.