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
        # does this key exist in the dictionary?
        if year in self.mass_dict:
            # is it a sub region measurement
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

        # what if the file path isn't a csv? will need to throw as error there 
        assert file_path.split(".")[-1] == 'csv', "please input a csv file"

        file_path = Path(file_path)
        self.file_path = file_path
        self.dict = {}
        # loading the data from the csv file
        with open(self.file_path, newline='') as file: 
            read_file = csv.reader(file)
            
            # skip the header of the csv file [check that the headings are in the expected order...] 
            next(read_file)
            for row in read_file:
                unit = row[0]
                name = row[1]
                idnt = row[2] 
                lat = float(row[5])
                lon = float(row[6])
                code = int(row[7]+row[8]+row[9])
                self.dict[idnt] = Glacier(idnt,name,unit,lat, lon, code)
        

    def read_mass_balance_data(self, file_path):
        # check that the user has inputed the right file extension 
        assert file_path.split(".")[-1] == 'csv', "please input a csv file"
        
        file_path = Path(file_path)

        with open(file_path, newline='') as file: 
            csv_reader = csv.reader(file)

            # skip the header of the csv file [ check that the headings are as expected...]
            next(csv_reader)
            for row in csv_reader:

                current_id = row[2]

                # is this a submeasurement
                if int(row[4]) != 9999:
                    submeasure = True
                else:
                    submeasure = False
                year = row[3]

                # is there a measurement for this year? 
                if row[-3] == "": 
                    balance = 0.0 
                else: 
                    balance = float(row[-3])
                self.dict[current_id].add_mass_balance_measurement(year, balance, submeasure)
                
                
            


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
