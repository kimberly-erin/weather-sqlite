from flask import Flask
from flask import json
from flask import jsonify
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine,func,desc

engine = create_engine("sqlite:///hawaii_sqlite.db")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurements = Base.classes.measurements

Stations=Base.classes.stations

session = Session(engine)

app = Flask(__name__)


@app.route("/api/v1.0/precipitation")
def precipitation():

    print("Server received request for /api/v1.0/precipitation")

    query_date=dt.datetime(2017,8,23)-dt.timedelta(days=365)
    
    query_results=session.\
    query(func.strftime('%Y-%m-%d',Measurements.date),Measurements.precipitation_tenths_of_mm).\
    filter(Measurements.date >= query_date).\
    all()

    return jsonify(dict(query_results))

@app.route("/api/v1.0/stations")
def stations():

    print("Server received request for /api/v1.0/stations")
    return jsonify(list(session.query(Stations.name,Stations.station)))

@app.route("/api/v1.0/tobs")
def tabs():
    query_date=dt.datetime(2017,8,23)-dt.timedelta(days=365)
    
    query_results=session.\
    query(Measurements.date,Measurements.station,Measurements.temp_observed).\
    filter(Measurements.date >= query_date).\
    all()

    print("Server received request for /api/v1.0/tobs")
    return jsonify(list(query_results))

@app.route("/api/v1.0/<start>")
def api(start):
    print("Server received request for 'api' page...")

    end=dt.datetime.today().date()

    return api2(start,start)
@app.route("/api/v1.0/<start>/<end>")
def api2(start,end):
    start_date=start
    end_date=end

    query_results=session.\
    query(func.min(Measurements.temp_observed),func.max(Measurements.temp_observed),func.avg(Measurements.temp_observed)).\
    filter(Measurements.date >= start_date).\
    filter(Measurements.date <= end_date).\
    group_by(Measurements.date).\
    all()

    print("Server received request for 'api2' page...")

    return jsonify(list(query_results))

if __name__ == "__main__":
    app.run(debug=True)
