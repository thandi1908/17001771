from pathlib import Path
import csv


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
                raise ValueError("csv missing column ", column)

