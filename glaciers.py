# -*- coding: utf-8 -*--v
from pathlib import Path

from _pytest.python_api import raises
import utils 
import csv 
import sys

import matplotlib.pyplot as plt

import datetime

from warnings import warn


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        # validate argument inputs
        if not isinstance(glacier_id, str):
            raise TypeError("Glacier id should be of type str")
        elif len(glacier_id) !=5:
            id_length = len(glacier_id) 
            raise ValueError("Expected glacier length of 5 but", id_length, "was given")
        elif not all(char.isdigit for char in glacier_id):
            raise ValueError("Glacier ID string must only contain digits")
        
       
        if not isinstance(name, str): 
            raise TypeError("Glacier Name should be string")
        
        if not isinstance(unit, str):
            raise TypeError("Glacier political unit should be a string")

        elif len(unit) != 2: 
            raise ValueError("Glacier political unit should have length 2")

        elif not unit.isupper():
            # check that its not the special case
            if unit !="99":
                raise ValueError("Glacier policitcal unit should be a 2 character string of uppercase letters or 99")
        
        utils.validate_lat_lon(lat, lon)

        if len(str(code)) != 3: 
            raise ValueError("Code should be of length 3")
        if not isinstance(code, int): 
            raise TypeError("Code should be an int")

        
        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat 
        self.lon = lon 
        self.code = code
        self.mass_balance = {}

    def add_mass_balance_measurement(self, year, mass_balance, subregion = False):
        # validating arguments
        current_year = datetime.datetime.now().year

        assert isinstance(mass_balance, (int, float)), "mass balance should be of type int or float"
        assert isinstance(subregion, bool), "subregion should be of type bool"

        if int(year) > current_year: 
            raise ValueError(str(int)+" is before the current year of "+str(current_year))

        # have we already got data for this year?
        if year in self.mass_balance:

            # is it a sub region measurement?
            if subregion == True and self.mass_balance[year]["subregion"] == True:
                self.mass_balance[year]["mass_balance"] += mass_balance
            
            # if it's not a subregion measurement but the previous was skip it
            elif subregion == False and self.mass_balance[year]["subregion"] ==True: 
                self.mass_balance[year]["mass_balance"] += 0 

        else: # new year measurement
            self.mass_balance[year] = {"mass_balance":mass_balance, "subregion": subregion}

    def plot_mass_balance(self, output_path):
        #validate path
        utils.validate_path(output_path)

        x_values = []
        y_values = []
        # make sure that the glacier has mass balance measurements
        if self.mass_balance: 
            for year in self.mass_balance:
                x_values.append(int(year))
                y_values.append(self.mass_balance[year]["mass_balance"])
            
            utils.mass_balance_plot(self, x_values, y_values, output_path)
        
        else:
            warn("This Glacier has no mass balance measurements")
            utils.mass_balance_plot(self, x_values, y_values, output_path)


        
class GlacierCollection:
    def __init__(self, file_path):

        utils.validate_path(file_path)

        self.file_path = file_path
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

        utils.validate_path(file_path)

        required_keys = ["WGMS_ID", "LOWER_BOUND", "YEAR", "ANNUAL_BALANCE"]
        # check_csv 
        utils.check_csv(file_path, required_keys)

        self.count = 0
        
        file_path = Path(file_path)

        with open(file_path, newline='') as file: 
            csv_reader = csv.DictReader(file)

            for row in csv_reader:

                current_id = row["WGMS_ID"]

                if not current_id in self.glaciers: 
                    raise ValueError("Glacier "+current_id+" is not in collection")

                # is this a submeasurement
                if int(row["LOWER_BOUND"]) != 9999:
                    submeasure = True
                else:
                    submeasure = False
                year = row["YEAR"]

                # is there a measurement for this year? 
                if row["ANNUAL_BALANCE"] == "": 
                    continue # ignore the row
                else: 
                    balance = float(row["ANNUAL_BALANCE"])
                    self.glaciers[current_id].add_mass_balance_measurement(year, balance, submeasure)
                    self.count += 1
                
                
            


    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        utils.validate_n(n, len(self.glaciers))
        utils.validate_lat_lon(lat,lon)

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
                    if int(code_pattern) == 0: 
                        raise ValueError("Code Pattern must be non-zero")
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
            if code_pattern == 0:
                raise ValueError("Code pattern must be non-zero")
            elif len(str(code_pattern)) != 3: 
                raise ValueError("Code pattern be 3 digits long")
            
            full_code = True
            
            # conduct search
            names = utils.search_by_code(self, code_pattern, full_code)

        else: 
            raise TypeError("Code pattern should be type int or str")

        return names


    def sort_by_latest_mass_balance(self, n=5, reverse=False):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        utils.validate_n(n, self.count)

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
        
        if reverse == False:
            # get a list of keys 
            keys = list(reversed(keys))[:n]
            for key in keys: 
                output_list.append(self.glaciers[key])
        
        elif reverse == True:
            keys = keys[:n]
            for key in keys:
                output_list.append(self.glaciers[key])
        return output_list

    def summary(self):
        if self.glaciers == False:
            raise ValueError("This collection is Empty")
        # print the number of glaciers in collection
        print("This collection has", len(self.glaciers), "glaciers")

        # tracking variables 
        earliest_year = sys.maxsize
        glacier_w_measure = 0 
        shrink = 0 
        grow = 0 

        for glacier in self.glaciers:
            glac = self.glaciers[glacier]

            # find the earliest measurement
            year_order = sorted(glac.mass_balance.keys(), key=lambda key: key)

            if len(year_order) != 0:
                year  = int(year_order[0]) 
                if int(year) <= earliest_year:
                    earliest_year = year

                # find out if the last measurement saw the glacier shrink
                latest_year = year_order[-1]
                mass_measurement = glac.mass_balance[latest_year]["mass_balance"]
                if mass_measurement < 0: 
                    shrink += 1
                else: 
                    grow += 1
                
                glacier_w_measure += 1
            else: 
                continue
        
        shrink_perc = int(round(100*shrink/glacier_w_measure))
        print("The earliest measurement was in", earliest_year)
        print(str(shrink_perc)+"% of glaciers shrunk in their last measurement")



    def plot_extremes(self, output_path):

        utils.validate_path(output_path)
        # tracking variables
        most_shrink = sys.maxsize
        shrink_id = None
        most_grow = - sys.maxsize
        grow_id = None

        for glacier in self.glaciers:
            glac = self.glaciers[glacier]
            
            #sort the years from oldest to most recent
            year_order = sorted(glac.mass_balance.keys(), key=lambda key: key)
            
            if len(year_order) != 0: # making sure the glacier has some measurements
                latest_year = year_order[-1]
                mass_measure = glac.mass_balance[latest_year]["mass_balance"]
                
                if mass_measure < 0 and mass_measure < most_shrink:
                    most_shrink = mass_measure
                    shrink_id = glacier
                
                elif mass_measure > 0 and mass_measure > most_grow:
                    most_grow = mass_measure
                    grow_id = glacier

        x_val_1 , x_val_2 = [], []
        y_val_1, y_val_2  = [], []

        glac_1 = self.glaciers[shrink_id]
        glac_2 = self.glaciers[grow_id]
        for year in glac_1.mass_balance:
                x_val_1.append(int(year))
                y_val_1.append(glac_1.mass_balance[year]["mass_balance"])
        
        for year in glac_2.mass_balance:
                x_val_2.append(int(year))
                y_val_2.append(glac_2.mass_balance[year]["mass_balance"])
                # print(y_val_2)

        # plotting
        plt.figure()
        plt.plot(x_val_1, y_val_1, '--', color = "crimson", label = "Most Shrinkage", alpha = 0.6)
        plt.plot(x_val_1, y_val_1, '+', color = "black", alpha = 0.6)

        plt.plot(x_val_2, y_val_2, '--', color = "lime", label = "Most Growth", alpha = 0.6)
        plt.plot(x_val_2, y_val_2, '+', color = "black", alpha = 0.6)

        plt.xlabel("Year")
        plt.ylabel("Mass Balance [mm.w.e]")
        plt.title("Glacier Collection Exteremes Plot")
        plt.legend()

        plt.savefig(output_path)

