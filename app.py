#setting up dependenices
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify

#===set up database===
#create engine to databse
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect database to a new base
Base = automap_base()
#reflect the tables
Base.prepare(engine,reflect=True)
#save tables into references
Mfake = Base.classes.measurement
Sfake = Base.classes.station

#===flask coding===
#generate app instance
app = Flask(__name__)

#define app and details

@app.route('/')
def homepage():
    #list all available routes
    return(f"Welcome API Homepage, please see below all available routes:<br/>"
           f"<br/>"
           f"Precipitation against dates: <a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
           f"<br/>"
           f"Station list:  <a href='http://127.0.0.1:5000/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
           f"<br/>"
           f"Temperature against dates observed</br>"
           f"by the most active station of last year:  <a href='http://127.0.0.1:5000/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
           f"<br/>"
           f"<br/>"
           f"NOTE: ========== For BELOW SECTION ==========<br/>"
           f"Please replace [YYYY-mm-dd] to your query dates, must be in YYYY-mm-dd format otherwise it will not proceed to result page!<br/>"
           f"<br/>"
           f"Temperature summary since given date(pop required date as in given format):  /api/v1.0/YYYY-mm-dd<br/>"
           f"<br/>"
           f"Temperature summary for a period(pop required dates as in given format):  /api/v1.0/YYYY-mm-dd/YYYY-mm-dd<br/>")
           
           

@app.route('/api/v1.0/precipitation')
def prcps():
    #create session
    session = Session(engine)
    #query for results
    result = session.query(Mfake.date,Mfake.prcp).order_by(Mfake.date).all()
    #close session
    session.close()
    #create a list to store dicts
    prcp_list=[]
    #put query data as 2 sets of key and values into a dict, and loop it for every queried paris, finally put dicts into the list
    for date,prcp in result:
        all_data={}
        all_data['date'] = date
        all_data['precipitation'] = prcp
        prcp_list.append(all_data)
    #show result in jsonified format
    return jsonify(prcp_list)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    result = session.query(Sfake.station,Sfake.name,Sfake.latitude,Sfake.longitude,Sfake.elevation).all()
    session.close()
    
    stat_list=[]
    
    for stat,name,lat,lon,ele in result:
        
        key_order = ['station','name','lat','lon','ele']
        all_stat = {}    
        all_stat['ele'] = ele
        all_stat['lon'] = lon
        all_stat['lat'] = lat
        all_stat['name'] = name
        all_stat['station'] = stat
        all_stat_ordered = {k:all_stat[k] for k in key_order}
        stat_list.append(all_stat_ordered)
    return jsonify(stat_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    most_active = session.query(Mfake.station,func.count(Mfake.station)).group_by(Mfake.station).\
                  order_by(func.count(Mfake.station).desc()).first().station
    enddate = session.query(Mfake.date).filter(Mfake.station == most_active).\
              order_by(Mfake.date.desc()).first().date
    startdate = dt.datetime.strptime(enddate,'%Y-%m-%d').date() - dt.timedelta(days=365)

    result = session.query(Mfake.date,Mfake.tobs).filter(Mfake.station == most_active).\
             filter(Mfake.date>=startdate).filter(Mfake.date<=enddate).all()
    
    session.close()

    temp_list=[]
    #different from the above, this time each dict only have 1 key and 1 value pair, and the rest are the same
    for date,temp in result:
        all_temp = {}
        all_temp[date] = temp
        temp_list.append(all_temp)

    return jsonify(temp_list)

@app.route('/api/v1.0/<start>')

def temstart(start):
    session=Session(engine)
    
    #find the earliest and latest dates within dataset 
    earliest = session.query(Mfake.date).order_by(Mfake.date).first().date
    latest = session.query(Mfake.date).order_by(Mfake.date.desc()).first().date
    #query for result based on the query date
    result = session.query(func.min(Mfake.tobs),func.max(Mfake.tobs),func.avg(Mfake.tobs)).filter(Mfake.date>=start).all()

    session.close()
    #set if statement in the case when querydate is out of range
    if start>=earliest and start<=latest:
        return(f'Temperature summary for {start} to latest:<br/>'
               f'Minimum Temperature is {round(result[0][0],2)} \N{degree sign}F<br/>'
               f'Maximum Temperature is {round(result[0][1],2)} \N{degree sign}F<br/>'
               f'Average Temperature is {round(result[0][2],2)} \N{degree sign}F')
    else:
        return(f'Error: Data not found. Please check:<br/>'
               f'1. Earliest date should not before 2010-01-01 and;<br/>'
               f'2. Latest date should not after 2017-08-23')     

@app.route('/api/v1.0/<start>/<end>')
def tempperiod(start,end):
    session = Session(engine)

    earliest = session.query(Mfake.date).order_by(Mfake.date).first().date
    latest = session.query(Mfake.date).order_by(Mfake.date.desc()).first().date

    result = session.query(func.min(Mfake.tobs),func.max(Mfake.tobs),func.avg(Mfake.tobs)).\
             filter(Mfake.date>=start).filter(Mfake.date<=end).all()       
    session.close()

    if start>=earliest and start<=latest and start<=end and end>=earliest and end<=latest:
        return(f'Temperature summary for {start} to {end}:<br/>'
               f'Minimum Temperature is {round(result[0][0],2)} \N{degree sign}F<br/>'
               f'Maximum Temperature is {round(result[0][1],2)} \N{degree sign}F<br/>'
               f'Average Temperature is {round(result[0][2],2)} \N{degree sign}F')
    else:
        return(f'Error: Data not found. Please check for your start and end dates:<br/>'
               f'1. Earliest date should not before 2010-01-01 and;<br/>'
               f'2. Latest date should not after 2017-08-23 and;<br/>'
               f'3. End date should later than or equal to start date') 
               
if __name__ == '__main__':
    app.run(debug=True)

