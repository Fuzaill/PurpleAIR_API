#Math functions for Project 3

import json
from collections import namedtuple
import math

#NamedTuples

LatLon = namedtuple('LatLon', ['lat', 'lon'])

#Functions

def convert_to_aqi(val: float) -> float:
    '''
    Converts the given value of AQI in PM2.5 and returns it as AQI.
    '''
    
    if val >= 0 and val < 12.1:
        c_high = 12.0
        c_low = 0
        a_high = 50
        a_low = 0

    elif val >= 12.1 and val < 35.5:
        c_high = 35.4
        c_low = 12.1
        a_high = 100
        a_low = 51

    elif val >= 35.5 and val < 55.5:
        c_high = 55.4
        c_low = 35.5
        a_high = 150
        a_low = 101

    elif val >= 55.5 and val < 150.5:
        c_high = 150.4
        c_low = 55.5
        a_high = 200
        a_low = 151

    elif val >= 150.5 and val < 250.5:
        c_high = 250.4
        c_low = 150.5
        a_high = 300
        a_low = 201

    elif val >= 250.5 and val < 350.5:
        c_high = 350.4
        c_low = 250.5
        a_high = 400
        a_low = 301

    elif val >= 350.5 and val < 500.5:
        c_high = 500.4
        c_low = 350.5
        a_high = 500
        a_low = 401

    elif val >= 500.5:
        return 501

    return aqi_formula(val, c_high, c_low, a_high, a_low)
    
def aqi_formula(c_input: float, c_high: float, c_low: float, a_high: float, a_low: float) -> int:
    '''
    The mathematical formula to calculate the aqi from the given parameters.
    Returns the rounded value of the AQI.
    '''

    x = a_high - a_low
    y = c_high - c_low
    z = c_input - c_low

    aqi = ((x/y)* z) + a_low

    if str(aqi).endswith('.5'):
        return round(aqi + 0.5)
    else:
        return round(aqi) 
    
 
def degree_to_radian(point: LatLon) -> LatLon:
    '''
    Converts the given LatLon object from degrees to radian and returns
    it. 
    '''
    
    lat_r = point.lat * (math.pi/180)
    lon_r = point.lon * (math.pi/180)

    return LatLon(lat = lat_r, lon = lon_r)

def lat_lon_distance(point_1: LatLon, point_2: LatLon) -> float:
    '''
    Computes the distance d between two coordinates and returns it.
    '''

    p1_r = degree_to_radian(point_1)
    p2_r = degree_to_radian(point_2)

    dlat = p1_r.lat - p2_r.lat
    dlon = p1_r.lon - p2_r.lon

    alat = (p1_r.lat + p2_r.lat) * 0.5
    
    R = 3958.8

    x = dlon * math.cos(alat)
    d = math.sqrt((x*x) + (dlat*dlat)) * R

    return d
