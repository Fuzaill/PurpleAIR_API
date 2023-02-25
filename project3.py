#main python file for project 3

import project3classes
import project3functions
import json
from collections import namedtuple
import math
from project3functions import LatLon

def run() -> None:
    '''
    Runs the main program.
    '''
    center = establish_center()
    search_range = get_range()
    threshold = get_threshold()
    max_n = get_max()
    aqi_data = get_aqi_data()
    reverse_files = get_reverse_files(max_n)

    display_center(center)

    data_list = compute_list(center, aqi_data, search_range, threshold)
    final_list = sort_and_shorten(data_list, max_n)
    location_list = get_reverse_locations(final_list, reverse_files)

    display_results(final_list, location_list)


def display_center(center: LatLon) -> None:
    '''
    Displays the first output; the coordinates of the center entered by
    the user. 
    '''
    
    print('CENTER ' + display_coordinates(center))


def display_coordinates(coordinates: LatLon) -> str:
    '''
    Formats the coordinates by taking the absolute value and
    concatinating their direction in a string. 
    '''
    clat = ''
    clon = ''
    
    if coordinates.lat >= 0:
        clat = str(coordinates.lat) + '/N'
    elif coordinates.lat < 0:
        clat = str(abs(coordinates.lat)) + '/S'

    if coordinates.lon >= 0:
        clon = str(coordinates.lon) + '/E'
    elif coordinates.lon < 0:
        clon = str(abs(coordinates.lon)) + '/W'
    
    return f'{clat} {clon}'                   

def display_results(final_list: [tuple], location_list: [str]) -> None:
    '''
    Displays the final results of the program. Outputs the AQI sensor
    data, the coordinates, and the location of the identified sensor.
    '''

    for i, x in enumerate(final_list):
        print('AQI ' + str(x[0]))
        print(display_coordinates(LatLon(x[1], x[2])))
        print(location_list[i])
    

def get_reverse_locations(final_list: [tuple], reverse_files: [str]) -> [str]:
    '''
    Aquires the results of the given coordinates via the Nominatim server
    or accesses the files to access the coordinates location. Returns a
    list of alphabetic locations of the cordinates. 
    '''

    location_list = []
    
    if len(reverse_files) == 0:
        for n in final_list:
            loc_data = project3classes.ReverseGeocodingNom(lat = n[1],lon = n[2])
            location_list.append(loc_data.location())
    else:
        for n in reverse_files:
            loc_data = project3classes.ReverseGeocodingFiles(n)
            location_list.append(loc_data.location())
    
    return location_list


def compute_list(center: LatLon, data: dict, s_range: int, aqi_threshold: int or float) -> list:
    '''
    Accesses the data obtained via Nominatim or private files and returns an
    unsorted list of tuples consisting the AQI sensor value, the latitude,and
    longitude of the location of the sensor that meet the threshold, range,
    and other criteria.
    '''

    unsorted_list = []
    for entry in data:
        if entry[25] == 0:
            if entry[4] <= 3600 and entry[4] != None:
                if entry[27] != None and entry[28] != None:                 
                    coordinates = LatLon(lat = entry[27], lon = entry[28])
                    distance = project3functions.lat_lon_distance(center, coordinates)
                    if distance <= s_range:
                        if entry[1] != None:
                            aqi_val = project3functions.convert_to_aqi(entry[1])
                            if aqi_val > aqi_threshold:
                                unsorted_list.append((aqi_val, entry[27], entry[28]))
                
    return unsorted_list


def sort_and_shorten(data_list: [tuple], max_n) -> [tuple]:
    '''
    Sorts the unsorted list and returns the highest values amongst the list.
    Returns no more than the max number of values specified for the output.
    '''

    data_list.sort(key = lambda data_list: data_list[0], reverse = True)
    new_list = []
    count = 0

    for n in data_list:
        new_list.append(n)
        count += 1
        if count == max_n:
            break
        
    return new_list
    

def establish_center() -> LatLon:
    '''
    Outputs a LatLon object depending on user input via Nominatim or
    a local json file.
    '''

    first = input()

    if first.startswith('CENTER NOMINATIM '):
        center = project3classes.GeocodingNominatim(first[17:])

    elif first.startswith('CENTER FILE '):
        center = project3classes.GeocodingFiles(first[12:])
        
    else:
        raise Exception
    
    return LatLon(lat = center.lat_f(), lon = center.lon_f())

def get_range() -> int:
    '''
    Takes the users input for the range and returns it. raises an
    exception if the format is incorrect.
    '''

    user_in = input()

    if user_in.startswith('RANGE '):
        return int(user_in[6:])
    else:
        raise Exception

def get_threshold() -> int:
    '''
    Takes the users input for the AQI threshold and returns it.
    Raises an error if the format is not valid.
    '''

    user_in = input()

    if user_in.startswith('THRESHOLD '):
        return int(user_in[10:])
    else:
        raise Exception

def get_max() -> int:
    '''
    Takes the users input for the max number of results to be
    outputted towards the end. Raises an error if the format is
    incorrect.
    '''

    user_in = input()

    if user_in.startswith('MAX '):
        return int(user_in[4:])
    else:
        raise Exception

def get_aqi_data() -> dict:
    '''
    Takes the users input to determine whether to access a local
    file or the Purple Air server for the AQI sensor data. 
    '''

    user_in = input()
    
    if user_in.startswith('AQI PURPLEAIR'):
        data = project3classes.AQIAPI()
        
    elif user_in.startswith('AQI FILE '):
        data = project3classes.AQIFILE(user_in[9:])
        
    else:
        raise Exception

    return data.data()

def get_reverse_files(max_n: int) -> list:
    '''
    Takes the users input to determine wheteher to access a local
    file or Nominatim for the Reverse Geocoding data. 
    '''

    user_in = input()
    
    if user_in.startswith('REVERSE NOMINATIM'):
        return []
    
    elif user_in.startswith('REVERSE FILES '):
        files = user_in[14:].split()
        if len(files) >= max_n:
            return files
        else:
            raise Exception
        
    else:
        raise Exception

if __name__ == '__main__':
    run()
