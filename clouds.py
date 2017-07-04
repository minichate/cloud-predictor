from flask import Flask
from flask import render_template
from datetime import datetime, timedelta, date
from pytz import timezone

app = Flask(__name__)

import math
def merc(lat, lon):
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x/lon
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + lat * (math.pi/180.0)/2.0)) * scale
    return (x, y)

@app.route("/")
def hello():
    data = []
    local = timezone('EST')
    utc = timezone('UTC')

    # bottem left -> top right corner
    #print merc(30, -108) + merc(44, -94)

    est_now = datetime.now()
    ust_today = local.localize(datetime(year=est_now.year, month=est_now.month, day=est_now.day)).astimezone(utc)

    if (est_now.hour < 13):
      generation_hours = 0
    else:
      generation_hours = 12
    
    hours_offset = generation_hours - 5

    generation = "%d%02d%02d%02d" % (est_now.year, est_now.month, est_now.day, generation_hours)

    for x in range(3, 49):
      data.append({
        'sequence': x,
        'start': ust_today + timedelta(hours=(x + hours_offset)),
        'end': ust_today + timedelta(hours=(x + hours_offset), minutes=59, seconds=59),
        'path': 'http://weather.gc.ca/data/prog/regional/%s/%s_054_R1_north@america@southeast_I_ASTRO_nt_0%02d.png' %(generation, generation, x)
      })
    return render_template('clouds.kml', data=data)
