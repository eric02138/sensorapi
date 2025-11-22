# SensorAPI
A minimal Flask backend that ingests sensor data 

## Design Considerations
I wanted to make setting up this demo as simple as possible, with minimal dependencies.  This actually led to more than a few headaches, namely connecting to the database (Flask *really* wants you to use SQLAlchemy) and the limitations of SQLite3 (which doesn't have a native DateTime field).  Using a NoSQL database like MongoDB might allow for greater flexibility were the application to grow.

## Installation
Create a virtual environment with a recent-ish version of Python 3 - I'm using Python 3.12.7.  Pyenv is nifty, too.
`pyenv virtualenv sensorapi`

Next, install the python packages we'll be using:
`pip install -r requirements.txt`
(This is old school - I like Poetry, but that's another install.)

