#Question 2: Temperature Analysis

'''
Create a program that analyses temperature data collected from multiple weather 
stations in Australia. The data is stored in multiple CSV files under a "temperatures" 
folder, with each file representing data from one year. Process ALL .csv files in the 
temperatures folder. Ignore missing temperature values (NaN) in calculations.
'''

#Import Temperature CSV Files and Operating Software for managing file paths.

import csv
import os

#Prompt for folder path
default_folder = "./temperatures/"
folder = input(f"Enter the path to your temperatures folder [{default_folder}]: ") or default_folder

#Get all CSV files in the folder
csv_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]

#Overall Temperature Analysis
all_temperatures = [] #Create list of temperatures

for filename in csv_files: #Begin loop of CSV Files
    if not os.path.exists(filename): #Ensure File exists
        print(f"File not found: {filename}")
        continue

    print(f"File Read: {filename}") 
    try:
        with open(filename, "r", encoding="utf-8") as file: #Read CSV File
            reader = csv.reader(file)
            header = next(reader)  #Ignore header row

            for row in reader:
                for value in row[4:]:  #Monthly temperatures (begin row 5)
                    if value.lower() != "nan" and value.strip() != "": #Ignore Nan and blank values
                        try:
                            temp = float(value)
                            all_temperatures.append(temp) #Add read Temperatures to All_temperatures list
                        except ValueError:
                            continue
    except Exception as e:
        print(f"Error read: {filename}: {e}") #For all exceptions create Error message

if all_temperatures:
    avg_temp = sum(all_temperatures) / len(all_temperatures)  #Measure Average temperature
    max_temp = max(all_temperatures) #Measure Max temperature
    min_temp = min(all_temperatures) #Measure Min temperature

    print(f"Temperature Analysis (For Period 1986–2005):")
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Max Temperature: {max_temp:.2f}°C")
    print(f"Min Temperature: {min_temp:.2f}°C")
    #Print Measurement Results
else:
    print("No valid temperature data found.")

#Station Temperature Range Analysis

station_temps = {}  #Ditionary: Station Name and Temperature
station_ids = {} #Dictionary: Station Name and ID

for filename in csv_files:  #Begin loop of CSV Files
    if not os.path.exists(filename): #Ensure File exists
        continue
    with open(filename, "r", encoding="utf-8") as file: #Open file to read
        reader = csv.reader(file) 
        next(reader)
        for row in reader: 
            name = row[0] #Header
            stn_id = row[1] #Station ID row
            station_ids[name] = stn_id
            for value in row[4:]: #Begin loop of Temperature values
                if value.lower() != "nan" and value.strip() != "": #Ignore Nan and blank values
                    try:
                        temp = float(value) #Convert to float to accept decimal figures
                        if name not in station_temps:
                            station_temps[name] = [] #If not in dictionary create new list item and add to dictionary
                        station_temps[name].append(temp)
                    except ValueError:
                        continue

#Calculate range per Station

station_ranges = {} #Dictionary for Sation range of temps
for name, temps in station_temps.items(): #Loop through Stations and temperatures
    if temps:
        min_t = min(temps) #Smallest temp recorded
        max_t = max(temps) #Largest temp recorded
        range_t = max_t - min_t #Calculate range of temps
        station_ranges[name] = (range_t, max_t, min_t) 

#Sort stations by range descending
sorted_stations = sorted(station_ranges.items(), key=lambda x: x[1][0], reverse=True)

#Save to txt file with Station ID, range, max temp and min temp.
with open("largest_temp_range_station.txt", "w") as out:
    out.write(f"Total stations analyzed: {len(sorted_stations)}\n\n")
    for name, (range_t, max_t, min_t) in sorted_stations:
        stn_id = station_ids.get(name, "Unknown")
        out.write(f"{name} (ID: {stn_id}): Range {range_t:.1f}°C (Max: {max_t:.1f}°C, Min: {min_t:.1f}°C)\n")

#Dictionary of months according to rows in CSV Files
season_names = {
    "Summer": [15, 4, 5],
    "Autumn": [6, 7, 8],
    "Winter": [9, 10, 11],
    "Spring": [12, 13, 14]
}

#Dictionary of Seasonal temperatures
season_temps = {season: [] for season in season_names}

for filename in csv_files: #loop through all CSV Files
    if not os.path.exists(filename):
        continue
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader: #for each season, look at specified season columns
            for season, indices in season_names.items():
                for i in indices:
                    if i < len(row):
                        value = row[i]
                        if value.lower() != "nan" and value.strip() != "":
                            try:
                                #Convert values to float and add to season temp list
                                season_temps[season].append(float(value))
                            except ValueError:
                                continue

#Save average seasonal temperatures to a text file
with open("average_temp.txt", "w") as out:
    for season, temps in season_temps.items():
        if temps:
            avg = sum(temps) / len(temps)  #Calculate average temps
            out.write(f"{season}: {avg:.1f}°C\n")

import math

#Dictionary to create SD for each station
station_SD = {}

#Loop through all CSV to calculate SD
for filename in csv_files:
    if not os.path.exists(filename): #Skip if file missing
        continue
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[0] #Station name is in first column
            temps = []
            #Loop through temp values
            for value in row[4:]:
                if value.lower() != "nan" and value.strip() != "":
                    try:
                        temps.append(float(value)) #Convert temp values to float
                    except ValueError:
                        continue
            if temps: #If station has temp data 
                mean = sum(temps) / len(temps) #Calculate average temp 
                variance = sum((t - mean) ** 2 for t in temps) / len(temps) #Calculate variance
                SD = math.sqrt(variance) #Calculate SD
                station_SD[name] = SD

#Calculate minimum and maximum SD values
min_std = min(station_SD.values())
max_std = max(station_SD.values())

#Calculate most and least stable stations
most_stable = [name for name, std in station_SD.items() if std == min_std]
most_variable = [name for name, std in station_SD.items() if std == max_std]

#Save SD data to a txt file
with open("temperature_stability_stations.txt", "w") as out:
    for name in most_stable:
        out.write(f"Most Stable: {name}: StdDev {min_std:.1f}°C\n")
    for name in most_variable:
        out.write(f"Most Variable: {name}: StdDev {max_std:.1f}°C\n")

        
