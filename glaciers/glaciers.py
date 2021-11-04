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

    def add_mass_balance_measurement(self, year, mass_balance, subregion = True):
        self.mass_dict[year] = {"mass_balance": mass_balance}

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:
    def __init__(self, file_path):
        file_path = Path(file_path)
        self.file_path = file_path
        self.dict = {}
        # what if the file path isn't a csv? will need to throw as error there 
        # loading the data from the csv file
        with open(self.file_path, newline='') as file: 
            read_file = csv.reader(file)
            
            # skip the header of the csv file
            next(read_file)
            for row in read_file:
                unit = row[0]
                name = row[1]
                idnt = row[2] 
                lat = row[5]
                lon = row[6]
                code = int(row[7]+row[8]+row[9])
                self.dict[idnt] = [Glacier(idnt,name,unit,lat, lon, code)]
        

    def read_mass_balance_data(self, file_path):
        file_path = Path(file_path)

        with open(file_path, newline='') as file: 
            csv_reader = csv.reader(file)

            # skip the header o the csv file
            next(csv_reader)

            # place holder variables 
            current_id = 0 
            current_year = 0 
            current_mass_balance = 0
            
            for row in csv_reader:

                if current_id == 0: 
                    current_id = row[2]
                    current_year = row[3]
                    print(row[-3])
                    current_mass_balance += row[-3]
                elif row[2] == current_id:
                    #same glacier different year
                    if row[3] != current_year:
                        self.dict[current_id].add_mass_balance_measurement(current_year, current_mass_balance)
                        current_year =row[3]
                        current_mass_balance = row[-3]
                    else:
                        # check if this is the final value
                        if row[5] == 9999:
                            current_mass_balance += 0
                        else: 
                            # same glacier same year
                            current_mass_balance += row[-3]

                else: 
                    # different glacier
                    current_id = row[2]
                    current_year = row[3]
                    current_mass_balance = row[-3]
            


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
