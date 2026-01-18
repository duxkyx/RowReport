from Telemetry.file_analyser import get_session_data
from Telemetry.section_data import section_rower_data, section_boat_data
from Telemetry.subroutines import convert


class Rower_Sampled_Data:
    def __init__(self):
        self.user_id = ''
        self.session_id = ''
        
        self.name = 'n/a'
        self.seat = 'n/a'
        self.side = 'n/a'
        self.strokes = 0

        # Initialize empty lists for sampled values
        self.min_angle = []
        self.max_angle = []
        self.arc_length = []
        self.catch_slip = []
        self.finish_slip = []
        self.rower_swivel_power = []
        self.seat_length = []
        self.power_timeline = []

        # 3D arrays
        self.gate_force_x = []
        self.gate_angle = []
        self.gate_angle_vel = []
        self.seat_posn = []
        self.seat_posn_vel = []
        self.body_arms_vel = []
        
        self.recovery_time_1 = []
        self.recovery_time_2 = []
        self.recovery_time_3 = []
        self.recovery_time_4 = []
        self.hang_time_1 = []
        self.hang_time_2 = []
        self.catch_slip_time = []
        self.drive_time_1 = []
        self.drive_time_2 = []
        self.drive_time_3 = []
        self.drive_time_4 = []
        self.finish_slip_time = []
        self.pause_time_1 = []
        self.pause_time_2 = []
        self.recovery_time_5 = []
        self.stroke_time = []
        self.drive_time = []
        self.recovery_time = []

        # Synchronisation
        self.difference_25 = []
        self.difference_50 = []
        self.difference_75 = []
        self.difference_hang = []
        self.difference_min = []
        self.difference_catch = []
        self.difference_effective_start = []
        self.difference_70max = []
        self.difference_maxf = []
        self.difference_max70 = []
        self.difference_effective_end = []
        self.difference_finish = []
        self.difference_max = []
        self.difference_recovery = []
        
    def to_dict(self):
        return self.__dict__
    
class boat_Sampled_Data:
    def __init__(self, boat_data):
        self.coach_id = ''

        self.description = ''
        self.state = ''
        self.filename = boat_data.FileName
        self.boatname = boat_data.BoatName
        self.category = boat_data.Category
        self.inboard = boat_data.Inboard
        self.oarlength = boat_data.OarLength
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

        self.rating = []
        self.averagepower = []
        self.distanceperstroke = []
        self.stroketime = []
        self.acceleration = []
        self.meterspersecond = []
        self.normalizedtime = []

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
        data_Save_Class = Rower_Sampled_Data()

        data_Save_Class.name = Rower.Name
        data_Save_Class.seat = Rower.Seat
        data_Save_Class.side = Rower.Side
        data_Save_Class.strokes = Rower.Recorded_Strokes

        list_Of_Rower_Data.append(section_rower_data(Rower.data, boat_data, data_Save_Class))

    # Setup class for sorted boat data.
    sorted_Boat_Data = section_boat_data(boat_data.data, boat_data, boat_Sampled_Data(boat_data))

    # Return the calculated data.
    return list_Of_Rower_Data, sorted_Boat_Data

    