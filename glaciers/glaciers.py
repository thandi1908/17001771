from pathlib import Path
import utils 
import csv 


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat 
        self.lon = lon 
        self.code = code

    def add_mass_balance_measurement(self, year, mass_balance):
        raise NotImplementedError

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):
        self.file_path = file_path
        self.dict = {}
        # what if the file path isn't a csv? will need to throw as error there 
        # loading the data from the csv file
        with open(self.file_path, newline='') as file: 
            read_file = csv.reader(file)
            for row in read_file:
                unit = row[0]
                name = row[1]
                idnt = row[2] 
                lat = row[5]
                lon = row[6]
                code = int(row[6]+row[7]+row[8])
                self.dict[idnt] = Glacier(id,name,unit,lat, lon, code)
        

    def read_mass_balance_data(self, file_path):
        raise NotImplementedError

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError
