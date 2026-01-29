# This file contains temporary classes to store boat and rower data during initialization.
# These classes are used to hold data before it is fully processed and integrated into the main application.

# Initiating the frame for storing overall boat | session data.
class Boat_Data():
    def __init__(self):
        self.FileName = 'n/a'
        self.BoatName = 'n/a'
        self.Category = 'n/a'
        self.Inboard = 'n/a'
        self.OarLength = 'n/a'
        self.Seats = 0
        self.tStrokes = 0
        self.Distance = 0
        self.timeElapsed = 0
        self.boatType = 'n/a'
        self.Date = 'n/a'
        self.Serial = 'n/a'
        self.Latitude = 0
        self.Longitude = 0
        self.Samples = 0
        self.SeatSensors = True
        
        self.data = {
            'Rating': [],
            'Average Power': [],
            'Distance / Stroke': [],
            'Stroke Time': [],
            'Acceleration': [],
            'Meters/s': [],
            'RollAngle': [],
            'PitchAngle': [],
            'YawAngle': [],
            'GPS': [],
            'Normalized Time': [],
        }

# Initiating the frame for storing individual seat (rower) data.
class Rower_Data():
    def __init__(self):
        self.Name = 'n/a'
        self.Side = 'n/a'
        self.Seat = 'n/a'
        self.Height = 1
        self.Weight = 1
        self.Recorded_Strokes = 0

        # Stores all values into one list for each section of data.
        self.data = {
            'MinAngle': [],
            'MaxAngle': [],
            'ArcLength': [],
            'Effective Length': [],
            'Effective MinAngle': [],
            'Effective MaxAngle': [],
            'CatchSlip': [],
            'FinishSlip': [],

            # Gate Angle Bar Plot
            'Recovery Time 1': [],
            'Recovery Time 2': [],
            'Recovery Time 3': [],
            'Recovery Time 4': [],
            'Hang Time 1': [],
            'Hang Time 2': [],
            'Catch Slip Time': [],
            'Drive Time 1': [],
            'Drive Time 2': [],
            'Drive Time 3': [],
            'Drive Time 4': [],
            'Finish Slip Time': [],
            'Pause Time 1': [],
            'Pause Time 2': [],
            'Recovery Time 5': [],
            'Stroke Time': [],
            'Total Drive Time': [],
            'Total Recovery Time': [],

            # Seat Bar Plot
            'Before Seat': [],
            'Seat Recovery': [],
            'Pause 1': [],
            'Pause 2': [],
            'Drive': [],
            'Drive Finished 1': [],
            'Drive Finished 2': [],

            # Common data
            'Rower Swivel Power': [],
            'Work Per Stroke': [],
            'GateForceX': [],
            'Normalized Time': [],
            'GateAngle': [],
            'GateAngleVel': [],
            'PercentOfArc': [],
            'PercentOfMaxForce': [],

            '70MaxGateForceX': [],
            'Angle_70MaxGateForceX': [],
            'MaxGateForceX': [],
            'AvgGateForceX': [],
            'Average Force / Max Force': [],
            'Angle_MaxGateForceX': [],
            'From70MaxGateForceX': [],
            'Angle_From70MaxGateForceX': [],

            # Seat data
            'SeatPosn': [],
            'SeatPosnVel': [],
            'SeatLength': [],
            'SeatMaxVel': [],
            'BodyArmsVel': [],

            'PercentageForce': [],
            'PercentageAngle': [],
            'Percentage70%MaxForce': [],

            'Position_Of_CSlip': [],
            'Position_Of_70MaxF': [],
            'Position_Of_MaxF': [],
            'Position_Of_From70MaxF': [],
            'Posititon_Of_FSlip': [],

            'Catch Force Gradient': [],
            'Finish Force Gradient': [],
            'Catch Factor': [],

            'Time_To_25%': [],
            'Time_To_50%': [],
            'Time_To_75%': [],
            'Time_To_Hang': [],
            'Time_To_Min': [],
            'Time_To_Catch': [],
            'Time_To_Effective_Start': [],
            'Time_To_70Max': [],
            'Time_To_MaxF': [],
            'Time_To_From70Max': [],
            'Time_To_Effective_End': [],
            'Time_To_Finish': [],
            'Time_To_Max': [],
            'Time_To_Recovery': [],

            'Difference_25': [],
            'Difference_50': [],
            'Difference_75': [],
            'Difference_Hang': [],
            'Difference_Min': [],
            'Difference_Catch': [],
            'Difference_Effective_Start': [],
            'Difference_70Max': [],
            'Difference_MaxF': [],
            'Difference_Max70': [],
            'Difference_Effective_End': [],
            'Difference_Finish': [],
            'Difference_Max': [],
            'Difference_Recovery': [],
        }