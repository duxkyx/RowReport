from Telemetry import colours
import statistics
from random import randint
import time

# Variables
seat_colours = colours.seat_colours
sample_colours = colours.sample_colours
markers = colours.markers
bar_colours = colours.bar_colours

def get_Line_Style(seat):
    ls = ''
    if int(seat) % 2 == 0:
        ls = 'dashed'
    else:
        ls = 'solid'
    return ls

def get_Line_Colour(seat):
    return seat_colours[str(seat)]

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

def crew_Average(data_Type, profiles_List):
    boat_Sum = 0
    total_Found = 0
    for rower_Stats in profiles_List:
        avg_Value = calculate_Average(rower_Stats.data[data_Type])
        boat_Sum += avg_Value
        total_Found += 1
    return float(boat_Sum / total_Found)

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

def get_Recorded_Meters(boatData):
    distance = get_Sum(boatData.data['Distance / Stroke'])
    return distance

def get_Meters_in_Sample(boatData, sample):
    distance = get_Sum(boatData.data['Distance / Stroke'])
    distance_per_sample = distance / boatData.Samples
    return ((distance_per_sample*(sample))-(distance_per_sample*(sample-1)))

def get_Meters_Sample_Text(boatData, sample):
    distance = get_Sum(boatData.data['Distance / Stroke'])
    distance_per_sample = distance / boatData.Samples
    string = f'{int(round(distance_per_sample*(sample-1),0))} m -> {int(round(distance_per_sample*(sample),0))} m'
    return string

# Returns an array which contains 8 other arrays which hold the sectioned data (not averaged).
# This data is seperated into 8 sections based on distance. (each array has no limit of values, just based on distance).
def section_List(data_List, boat_Data):
    sectioned_List = []
    elements_Per_Section = []
    stroke_Distances = boat_Data.data['Distance / Stroke']
    total_Distance = get_Sum(stroke_Distances)

    iterations = 0
    for x in range(8):
        total = 0
        elements = 0
        for i in range(iterations, len(stroke_Distances)):
            distance = stroke_Distances[i]
            if total < total_Distance/8:
                total += distance
                elements += 1
            else:
                break
            iterations += 1
        if elements != 0:
            elements_Per_Section.append(elements)

    incrementer = 0
    iterate = 0
    for i in elements_Per_Section:
        section = []
        sum = 0
        for f in range(0, iterate):
            sum += elements_Per_Section[f]
        for x in range(incrementer, (i+sum)):
            value = data_List[x]
            section.append(value)
            incrementer += 1
        iterate += 1

        sectioned_List.append(section)

    if boat_Data.Samples == 0:
        boat_Data.Samples = len(sectioned_List)

    return sectioned_List

# Returns an array of 8 values.
def section_Data(data_List, boat_Data, get_Size=False):
    elements_In_Sample = []
    sectioned_Data = []
    sectioned_List = section_List(data_List, boat_Data)

    for section in sectioned_List:
        average = calculate_Average(section)
        elements_In_Sample.append(len(section))
        sectioned_Data.append(average)

    if get_Size == True:
        return sectioned_Data, elements_In_Sample

    return sectioned_Data

def average_Array_into_Sections(data_List):
    averaged_Sections = []

    for array_Container in data_List:
        average_Of_Container = []

        for i in range(0,len(array_Container[0])):
            numbers_of_scanned_index = []
            for sectioned_Array in array_Container:
                try:
                    numbers_of_scanned_index.append(sectioned_Array[i])
                except: pass
            average = calculate_Average(numbers_of_scanned_index)
            average_Of_Container.append(average)

        averaged_Sections.append(average_Of_Container)

    return averaged_Sections

# This subroutine takes an array which has more than one array contained inside (as a child)
# These sub arrays are looped and create a new single list which is an average of both.
def average_Array_into_One(data_List):
    averaged_List = []

    list_of_array_lengths = []
    for array in data_List:
        length = len(array)
        list_of_array_lengths.append(length)

    average_List_Length = int(calculate_Average(list_of_array_lengths))

    for i in range(0,average_List_Length):
        number_of_scanned_index = []
        for array in data_List:
            try:
                number_of_scanned_index.append(array[i])
            except: pass
        average = calculate_Average(number_of_scanned_index)
        averaged_List.append(average)

    return averaged_List

def average_Array_into_One_Percentage(data_list):
    averaged_list = []

    # Step 1: find the maximum length of the arrays
    max_length = max(len(arr) for arr in data_list if arr)

    # Step 2: average across arrays index by index
    for i in range(max_length):
        values_at_i = [arr[i] for arr in data_list if i < len(arr)]
        if values_at_i:
            averaged_list.append(sum(values_at_i) / len(values_at_i))

    # Step 3: normalize to 0–100
    if averaged_list:
        old_min, old_max = min(averaged_list), max(averaged_list)
        if old_max != old_min:  # avoid div by zero
            averaged_list = [
                (x - old_min) / (old_max - old_min) * 100
                for x in averaged_list
            ]
        else:
            averaged_list = [0 for _ in averaged_list]

    return averaged_list

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

# Check if input is a 2D list
def is_2d_list(lst):
    return (
        isinstance(lst, list) and
        all(isinstance(i, list) for i in lst) and
        all(not isinstance(j, list) for i in lst for j in i)
    )

# Seconds to hours
def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

# Sample rate = 0.02, 1 / 50hz
def calculate_time(length):
    number_of_intervals = length-1
    return float(number_of_intervals * 0.02) * 1000