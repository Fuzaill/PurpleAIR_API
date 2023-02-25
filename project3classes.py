import json
import urllib.parse
import urllib.request
import time

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#TODO LIST
#REMOVE SSL at the end
# 'https://nominatim.openstreetmap.org/search?'

class GeocodingNominatim:
    def __init__(self, location: str):
        
        base_url = 'https://nominatim.openstreetmap.org/search?'
        url_location = ([('q',location),('format','json')])
        self._url =  base_url + urllib.parse.urlencode(url_location)
        referer = 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/sfali1'
        req = urllib.request.Request(self._url, headers = {'Referer': referer })
        res = None
        try:
            res = urllib.request.urlopen(req)
            data = res.read()
            text = data.decode(encoding = 'utf-8')
            try:
                self._text = json.loads(text)
                if len(self._text) == 0:
                    print('FAILED')
                    print(f'{res.status} {self._url}')
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(f'{res.status} {self._url}')
                print('FORMAT')
                
            
        except urllib.error.HTTPError as e:
            x = e
            print('FAILED')
            print(f'{x.code} {self._url}')
            print('NOT 200')
            

        except urllib.error.URLError as e:
            x = e
            print('FAILED')
            print(f'{self._url}')
            print('NETWORK')
            
        if res != None:
            res.close()
        
    def lat(self) -> str:
        '''
        Returns latitude in string type.
        '''
    
        return self._text[0]['lat'] 

    def lon(self) -> str:
        '''
        Returns longitude in string type.
        '''

        return self._text[0]['lon']

    def lat_f(self) -> float:
        '''
        Returns latitude in float type.
        '''
        return float(self._text[0]['lat'])

    def lon_f(self) -> float:
        '''
        Returns longitude in float type.
        '''
        return float(self._text[0]['lon'])
        
class GeocodingFiles:
    def __init__(self, file: str):
        
        f = None

        try:
            f = open(file, encoding='utf8')
            try:
                self._text = json.load(f)
                if len(self._text) == 0:
                    print('FAILED')
                    print(file)
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(file)
                print('FORMAT')

        except OSError:
            print('FAILED')
            print(file)
            print('MISSING')

        except ValueError:
            print('FAILED')
            print(file)
            print('FORMAT')

        if f != None:
            f.close()

    def lat(self) -> str:
        '''
        Returns the latitude in string type.
        '''
    
        return self._text[0]['lat'] 

    def lon(self) -> str:
        '''
        Returns the longitude in string type.
        '''

        return self._text[0]['lon']

    def lat_f(self) -> float:
        '''
        Returns the latitude in float type.
        '''
        return float(self._text[0]['lat'])

    def lon_f(self) -> float:
        '''
        Returns the longitude in float type.
        '''
        return float(self._text[0]['lon'])


class AQIAPI:

    def __init__(self):

        req = urllib.request.Request('https://www.purpleair.com/data.json')
        res = None
        self._text = None
        try:
            res = urllib.request.urlopen(req)
            data = res.read()
            text = data.decode(encoding = 'utf-8')
            try:
                self._text = json.loads(text)
                if len(self._text) == 0:
                    print('FAILED')
                    print(f'{res.status} {self._url}')
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(f'{res.status} {self._url}')
                print('FORMAT')
                
            
        except urllib.error.HTTPError as e:
            x = e
            print('FAILED')
            print(f'{x.code} {self._url}')
            print('NOT 200')
            

        except urllib.error.URLError as e:
            x = e
            print('FAILED')
            print(f'{self._url}')
            print('NETWORK')
            
        if res != None:
            res.close()


    def data(self) -> dict:
        '''
        Returns the dictionary of sensor data. 
        '''
        return self._text['data']


class AQIFILE:

    def __init__(self, file):

        f = None

        try:
            f = open(file, encoding='utf8')
            try:
                self._text = json.load(f)
                if len(self._text) == 0:
                    print('FAILED')
                    print(file)
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(file)
                print('FORMAT')
                

        except OSError:
            print('FAILED')
            print(file)
            print('MISSING')

        except ValueError:
            print('FAILED')
            print(file)
            print('FORMATT')

        if f != None:
            f.close()


    def data(self) -> dict:
        '''
        Returns the dictionary of sensor data.
        '''
        return self._text['data']


class ReverseGeocodingNom:

    def __init__(self, lat, lon):
        time.sleep(1)
        base_url = 'https://nominatim.openstreetmap.org/reverse?'
        url_location = ([('lat',lat),('lon', lon), ('format', 'json')])
        self._url =  base_url + urllib.parse.urlencode(url_location)
        referer = 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/sfali1'
        req = urllib.request.Request(self._url, headers = {'Referer': referer })
        res = None
        try:
            res = urllib.request.urlopen(req)
            data = res.read()
            text = data.decode(encoding = 'utf-8')
            try:
                self._text = json.loads(text)
                if len(self._text) == 0:
                    print('FAILED')
                    print(f'{res.status} {self._url}')
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(f'{res.status} {self._url}')
                print('FORMAT')
            
        except urllib.error.HTTPError as e:
            x = e
            print('FAILED')
            print(f'{x.code} {self._url}')
            print('NOT 200')
            

        except urllib.error.URLError as e:
            x = e
            print('FAILED')
            print(f'{self._url}')
            print('NETWORK')
            
        if res != None:
            res.close()
        
    def location(self) -> str:
        '''
        Returns the name of the location.
        '''
        return self._text['display_name']


class ReverseGeocodingFiles:

    def __init__(self, file):

        f = None

        try:
            f = open(file, encoding='utf8')
            try:
                self._text = json.load(f)
                if len(self._text) == 0:
                    print('FAILED')
                    print(file)
                    print('FORMAT')
                    
            except json.decoder.JSONDecodeError:
                print('FAILED')
                print(file)
                print('FORMAT')

        except OSError:
            print('FAILED')
            print(file)
            print('MISSING')

        except ValueError:
            print('FAILED')
            print(file)
            print('FORMATT')

        if f != None:
            f.close()


    def location(self) -> str:
        '''
        Returns the name of the location.
        '''
        return self._text['display_name']
    
