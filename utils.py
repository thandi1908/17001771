from pathlib import Path
import csv
import re 
from math import sin, cos, sqrt, asin, radians


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    assert isinstance(lat1, (float, int)) and isinstance(lat2, (float, int)) , "Latitude should be of type int or float"

    assert isinstance(lon1, (float, int)) and isinstance(lon2, (float, int)) , "Longitude should be of type int or float"

    if lat1 < -90 or lat1 > 90: 
        raise ValueError("Latitude should be in range [-90, 90], but", lat1, " was given")
    elif lat2< -90 or lat2 > 90: 
        raise ValueError("Latitude should be in range [-90, 90], but", lat2, " was given")

    if lon1 < -180 or lon1 > 180: 
        raise ValueError("Longitude should be in range [-180, 180] but", lon1, " was given") 
    elif lon2 < -180 or lon2 > 180: 
        raise ValueError("Longitude should be in range [-180, 180] but", lon2, " was given") 
    
    # convert the lats and longs into radians
    lat1, lon1 = radians(lat1), radians(lon1)

    lat2, lon2 = radians(lat2), radians(lon2)

    R = 6371

    sine_term_1 = sin((lat2 - lat1)/2)**2

    cos_term_2 = cos(lat1)*cos(lat2)
    sin_term_2 = sin((lon2-lon1)/2)**2
    term_2 = cos_term_2*sin_term_2
    bracket = sqrt(sine_term_1 + term_2)

    return 2*R*asin(bracket)

def check_csv(file_path, required_keys):

    '''
    Function for checking that the CSV files are as expected
    '''
    # validating inputs

    if not isinstance(file_path, Path): 
        raise TypeError("output path should be a Path Object")
   
    assert isinstance(required_keys, (list, tuple)), "required keys should be a list or tuple"
    
    # Check file extension
    full_path = file_path.absolute()
    str_path = full_path.as_posix()
    
    assert str_path.split(".")[-1] == 'csv', "please input a csv file"

    with open(file_path, newline='') as file: 
        read_file = csv.DictReader(file)
        check_columns = dict(list(read_file)[0])

        for column in required_keys:
            if column not in check_columns:
                raise TypeError("csv missing column ", column)

def search_by_code(collection, code_pattern, full_code):
    
    # validating inputs
    assert isinstance(full_code, bool)

    assert isinstance(code_pattern, (str,int))

    # empty list of codes
    names = []
    if full_code:
        for key in collection.glaciers:
            if collection.glaciers[key].code == code_pattern:
                names.append(collection.glaciers[key].name)
        
    else: # wildcard 
        # where in the string is the digit
        pos = []
        search = re.compile(r"\d")
        for d in search.finditer(code_pattern):
            pos.append(d.start())
        
        # can have one or two digits
        if len(pos) == 1:
            indx = pos[0]
            for key in collection.glaciers:
                if str(collection.glaciers[key].code)[indx] == code_pattern[indx]:
                    names.append(collection.glaciers[key].name)
                    print(collection.glaciers[key].code)
        
        # searing for 2 digits provided
        elif len(pos) == 2:
            indx_0, indx_1 = pos[0], pos[1]
            for key in collection.glaciers:
                g_code = str(collection.glaciers[key].code)
                if g_code[indx_0] == code_pattern[indx_0] and g_code[indx_1] == code_pattern[indx_1]:
                    names.append(collection.glaciers[key].name)
                    # print(g_code)

    # return the names of the glaciers with that matching name 
    print("Number of matching glaciers:", len(names))
    return names
