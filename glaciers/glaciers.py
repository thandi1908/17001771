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
        self.mass_dict = {}

    def add_mass_balance_measurement(self, year, mass_balance, subregion = False):

        # have we already got data for this year?
        if year in self.mass_dict:

            # is it a sub region measurement?
            if subregion == True and self.mass_dict[year]["subregion"] == True:
                self.mass_dict[year]["mass_balance"] += mass_balance
            
            # if it's not a subregion measurement but the previous was skip it
            elif subregion == False and self.mass_dict[year]["subregion"] ==True: 
                pass 

        else: # new year measurement
            self.mass_dict[year] = {"mass_balance":mass_balance, "subregion": subregion}

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:
    def __init__(self, file_path):

        self.file_path = Path(file_path)
        self.glaciers = {}

        # required keys
        required_keys = ["POLITICAL_UNIT", "NAME",
         "WGMS_ID", "LATITUDE", "LONGITUDE",
         "PRIM_CLASSIFIC","FORM", "FRONTAL_CHARS"]

        # check_csv 
        utils.check_csv(file_path, required_keys)

        # loading the data from the csv file
        with open(self.file_path, newline='') as file: 
            read_file = csv.DictReader(file)

            for row in read_file:
                unit = row["POLITICAL_UNIT"]
                name = row["NAME"]
                idnt = row["WGMS_ID"] 
                lat = float(row["LATITUDE"])
                lon = float(row["LONGITUDE"])
                code = int(row["PRIM_CLASSIFIC"]+row["FORM"]+row["FRONTAL_CHARS"])
                self.glaciers[idnt] = Glacier(idnt,name,unit,lat, lon, code)
        

    def read_mass_balance_data(self, file_path):

        required_keys = ["WGMS_ID", "LOWER_BOUND", "YEAR", "ANNUAL_BALANCE"]
        # check_csv 
        utils.check_csv(file_path, required_keys)
        
        file_path = Path(file_path)

        with open(file_path, newline='') as file: 
            csv_reader = csv.DictReader(file)

            for row in csv_reader:

                current_id = row["WGMS_ID"]

                # is this a submeasurement
                if int(row["LOWER_BOUND"]) != 9999:
                    submeasure = True
                else:
                    submeasure = False
                year = row["YEAR"]

                # is there a measurement for this year? 
                if row["ANNUAL_BALANCE"] == "": 
                    balance = 0.0 
                else: 
                    balance = float(row["ANNUAL_BALANCE"])
                self.glaciers[current_id].add_mass_balance_measurement(year, balance, submeasure)
                
                
            


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

test = GlacierCollection("/Users/thandikiremadula/Desktop/17001771/glaciers/sheet-A.csv")
test.read_mass_balance_data("/Users/thandikiremadula/Desktop/17001771/glaciers/sheet-EE.csv")
