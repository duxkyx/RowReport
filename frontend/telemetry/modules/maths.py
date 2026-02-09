# This file holds various mathematical subroutines used across the telemetry frontend.

import statistics
import time

def calculate_Average(data_List):
    sum = 0
    total_Recorded = 0

    for value in data_List:
        try:
            sum += float(value)
            total_Recorded += 1
        except:
            continue

    average = (sum / total_Recorded)
    return round(average,3)

def get_Sum(array):
    sum = 0
    for i in array:
        sum += i
    return sum

def calculate_Percentage(original, new):
    return round(((new/original) * 100),3)

def calcuate_SD(array):
    sd = statistics.stdev(array)
    return round(sd,3)

def calculate_Variation(array):
    integer_Array = []
    for index in array:
        integer_Array.append(float(index))
    largest = max(integer_Array)
    smallest = min(integer_Array)
    difference = largest - smallest
    return round(difference,3)

def crew_Average(data_Type, profiles_List):
    boat_Sum = 0
    total_Found = 0
    for rower_Stats in profiles_List:
        avg_Value = calculate_Average(rower_Stats.data[data_Type])
        boat_Sum += avg_Value
        total_Found += 1
    return float(boat_Sum / total_Found)

def find_seat_Position_In_Array(seat, profiles):
    index = 0
    for profile in profiles:
        if int(profile.Seat) == int(seat):
            return index
        index += 1

def find_Column_Position(name, grid, Column_Name_Line):
    incrementer = 0
    for column in grid[Column_Name_Line]:
        if column == name:
            return incrementer
        incrementer += 1

# This function gets the time in seconds based on the length of an array.
# Sample rate = 0.02, 1 / 50hz
def calculate_time(length):
    number_of_intervals = length-1
    calculatedTime = float(number_of_intervals * 0.02) * 1000
    return calculatedTime

# Seconds to hours
def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
