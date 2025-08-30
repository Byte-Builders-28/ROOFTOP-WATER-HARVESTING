from . import models

# CRUD operations for the database ... All handled..

def save_groundwater(db, location, level, date):
    gw = models.GroundWater(location=location, level=level, date=date)
    db.add(gw)
    db.commit()
    db.refresh(gw)
    return gw

def save_weather(db, district, forecast, timestamp):
    w = models.Weather(district=district, forecast=forecast, timestamp=timestamp)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w
