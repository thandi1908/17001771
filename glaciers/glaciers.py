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
        self.mass_balance = {}

    def add_mass_balance_measurement(self, year, mass_balance, subregion = False):

        # have we already got data for this year?
        if year in self.mass_balance:

            # is it a sub region measurement?
            if subregion == True and self.mass_balance[year]["subregion"] == True:
                self.mass_balance[year]["mass_balance"] += mass_balance
            
            # if it's not a subregion measurement but the previous was skip it
            elif subregion == False and self.mass_balance[year]["subregion"] ==True: 
                pass 

        else: # new year measurement
            self.mass_balance[year] = {"mass_balance":mass_balance, "subregion": subregion}

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
                    pass # ignore the row
                else: 
                    balance = float(row["ANNUAL_BALANCE"])
                    self.glaciers[current_id].add_mass_balance_measurement(year, balance, submeasure)
                
                
            


    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        # TODO: Validate inputs
        distance_dict = {} 

        for key in self.glaciers:
            temp_glacier = self.glaciers[key]
            lat2, lon2 = temp_glacier.lat, temp_glacier.lon
            distance = utils.haversine_distance(lat,lon, lat2, lon2)
            distance_dict[temp_glacier.name] = distance
        
        # sort dict into order of value from least to greatest
        distance_dict = dict(sorted(distance_dict.items(), key=lambda item: item[1]))

        names = list(distance_dict.keys())[:n]
        return names
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        # is the code  a string? 
        if isinstance(code_pattern, str):
            # make sure the user has inputted the right code length
            if len(code_pattern) != 3: 
                raise ValueError("Code pattern must be have 3 chars long")

            #is it all a mixture of numbers and question marks?
            if all( (char.isdigit() or char =='?') for char in code_pattern):

                # if it's all question marks throw an error
                if all((char == "?") for char in code_pattern):
                    raise ValueError("Need atleast one digit in code pattern")
                
                # is it all digits? 
                elif all(char.isdigit() for char in code_pattern):
                    full_code = True 
                    code_pattern = int(code_pattern)
                    # conduct_search
                    names = utils.search_by_code(self, code_pattern, full_code)

                else: # is it a mixture
                    full_code = False
                    
                    # conduct search
                    names = utils.search_by_code(self, code_pattern, full_code)

            else: 
                raise ValueError("Code pattern must contain only digits and ?")
        
        elif isinstance(code_pattern, int):
            # make sure inputted string has the right length
            if len(str(code_pattern)) != 3: 
                raise ValueError("Code pattern be 3 digits long")
            
            full_code = True
            
            # conduct search
            names = utils.search_by_code(self, code_pattern, full_code)

        else: 
            raise TypeError("Code pattern should be type int or str")

        return names


    def sort_by_latest_mass_balance(self, n=5, reverse=False):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        
        # create glacier dictionary with only latest mass_balance measurement
        smaller_dict = {}
        
        for glacier in self.glaciers:
            glac = self.glaciers[glacier]
            
            #sort the years from oldest to most recent
            year_order = sorted(glac.mass_balance.keys(), key=lambda key: key)
            
            if len(year_order) != 0: # making sure the glacier has some measurements
                latest_year = year_order[-1]
                smaller_dict[glacier] = glac.mass_balance[latest_year]["mass_balance"]
            else: 
                continue

        # order the dictionary in order of smallest to largest change 
        smaller_dict = dict(sorted(smaller_dict.items(), key=lambda item: item[1]))

        output_list = []
        keys = list(smaller_dict.keys())
        if not reverse:
            # get a list of keys 
            keys = keys[-n:]
            for key in keys: 
                output_list.append(self.glaciers[key])
        else: 
            keys = keys[:n]
            for key in keys:
                output_list.append(self.glaciers[key])
        print(output_list)
        return output_list

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError

test = GlacierCollection("/Users/thandikiremadula/Desktop/17001771/glaciers/sheet-A.csv")
test.read_mass_balance_data("/Users/thandikiremadula/Desktop/17001771/glaciers/sheet-EE.csv")
test.sort_by_latest_mass_balance(n=1)
