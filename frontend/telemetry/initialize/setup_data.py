from telemetry.initialize.file_analyser import get_session_data
from telemetry.initialize.section_data import section_rower_data, section_boat_data
from telemetry.modules.maths import convert, get_Sum
from telemetry.modules.sorting import section_List

# Athlete Data Class -> Holds data to be stored in database.
class athlete_db_ready_data:
    def to_dict(self):
        return self.__dict__

# Session Data Class -> Holds data to be stored in database.
class session_db_ready_data:
    def __init__(self, boat_data):
        self.coach_id = ''
        self.description = ''
        self.state = ''
        self.filename = boat_data.FileName
        self.boatname = boat_data.BoatName
        self.category = boat_data.Category
        self.seats = boat_data.Seats
        self.tstrokes = boat_data.tStrokes
        self.distance = boat_data.Distance
        self.timeelapsed = convert(boat_data.timeElapsed) # Converts to string format
        self.boattype = boat_data.boatType
        self.date = boat_data.Date
        self.serial = boat_data.Serial
        self.latitude = boat_data.Latitude
        self.longitude = boat_data.Longitude
        self.seat_sensors = boat_data.SeatSensors
        self.inboard = boat_data.Inboard
        self.oarlength = boat_data.Outboard

        self.rating = []
        self.averagepower = []
        self.distanceperstroke = []
        self.stroketime = []
        self.meterspersecond = []
        self.normalizedcatch = []
        self.normalizedfinish = []
        self.sample_time = []
        self.sample_strokes = []
        self.acceleration = []
        self.normalizedtime = []
        self.boatroll = []
        self.boatpitch = []
        self.boatyaw = []
        self.gps = []

    def to_dict(self):
        return self.__dict__

def set_session_classes(file):
    class_data = get_session_data(file)

    # Define the data from the file calculations.
    user_data = class_data[0]
    boat_data = class_data[1]

    # Collect all sorted user (rower) data.
    list_Of_Rower_Data = []
    for Rower in user_data:
        data_Save_Class = athlete_db_ready_data()

        data_Save_Class.name = Rower.Name
        data_Save_Class.seat = Rower.Seat
        data_Save_Class.side = Rower.Side
        data_Save_Class.strokes = Rower.Recorded_Strokes

        list_Of_Rower_Data.append(section_rower_data(Rower.data, boat_data, data_Save_Class))

    # Free up memory - clear large data list from file_analyser.py after data is calculated.
    user_data.clear()

    # Setup class for sorted boat data.
    sorted_Boat_Data = section_boat_data(boat_data.data, boat_data, session_db_ready_data(boat_data))

    sorted_Boat_Data.sample_strokes = section_List(boat_data.data['Stroke Time'], boat_data, True)
    sectioned_Stroke_Times = section_List(boat_data.data['Stroke Time'], boat_data)

    # Free up memory - Boat_Data
    boat_data = []

    sample_Times = []
    for list in sectioned_Stroke_Times:
        sum = get_Sum(list)
        sample_Times.append(sum)

    sorted_Boat_Data.sample_time = sample_Times

    # Return the calculated data.
    return list_Of_Rower_Data, sorted_Boat_Data

    