from pathlib import Path
import csv
import re 


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    raise NotImplementedError

def check_csv(file_path, required_keys):

    '''
     DOC STRING 
    '''
    
    assert file_path.split(".")[-1] == 'csv', "please input a csv file"

    file_path = Path(file_path)

    with open(file_path, newline='') as file: 
        read_file = csv.DictReader(file)
        check_columns = dict(list(read_file)[0])

        for column in required_keys:
            if column not in check_columns:
                raise TypeError("csv missing column ", column)

def search_by_code(collection, code_pattern, full_code):
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
        
        # searing for 2 digits provided
        elif len(pos) == 2:
            indx_0, indx_1 = pos[0], pos[1]
            for key in collection.glaciers:
                g_code = str(collection.glaciers[key].code)
                if g_code[indx_0] == code_pattern[indx_0] and g_code[indx_1] == code_pattern[indx_1]:
                    names.append(collection.glaciers[key].name)

    # return the names of the glaciers with that matching name 
    print("Number of matching glaciers:", len(names))
    return names
