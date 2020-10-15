import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connect_args={'check_same_thread':False}

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
# 2. Create an app, being sure to pass __name__
# For details on this, see: http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
app = Flask(__name__)

#variable for two date marks
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
latest_date = dt.date(2017,8,23)

# 3. Define what to do when a user hits the index route
# These `@app.route` lines are called "decorators" and are used to define 
# the a response for a specific URL route.
@app.route("/")
def Welcome():
    return "Welcome to Hawaii Weather API!"

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    latest_date = dt.date(2017,8,23)

    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).filter(Measurement.date <= latest_date).all()
    
    session.close()

    return jsonify(dict(prcp_scores))


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_names = session.query(Measurement.station).group_by(Measurement.station).all()
    
    session.close()

    station_results = list(np.ravel(station_names))

    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    latest_date = dt.date(2017,8,23)

    tobs_list = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= year_ago).filter(Measurement.date <= latest_date).all()
    
    session.close()

    return jsonify(tobs_list)



@app.route("/api/v1.0/start/<start>")
def start(start):

    session = Session(engine)

    temps = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    return jsonify(temps)

@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    end_temps = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    end_temps_list = list(np.ravel(end_temps))

    return jsonify(end_temps_list)




# This final if statement simply allows us to run in "Development" mode, which 
# means that we can make changes to our files and then save them to see the results of 
# the change without restarting the server.
# explanation of the line below: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app.run(debug=True)