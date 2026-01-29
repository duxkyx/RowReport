from telemetry.graphs.colours import colours
from telemetry.modules.maths import get_Sum

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