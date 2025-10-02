# Peach Telemetry data analysis program | Developed by Ben Loggie
# This program file will take the found file and convert it into a grid format, this grid is then searched and calculations are made to find the relevent data.

import Telemetry.subroutines as Subroutines
import math

def get_session_data(file):
    grid = []
    profiles_List = []
    strokes_Skipped = [] # Holds the iteration count for the stroke not recorded (not full normalized time)
    boat_Data = None

    getPercentage = Subroutines.calculate_Percentage
    getAverage = Subroutines.calculate_Average

    """
    This section defines the classes which will be used to store each individual seats data from the boat.
    """

    # Initiating the frame for storing boat data.
    class Boat_Data():
        def __init__(self):
            self.FileName = file.filename
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
                'Difference_Recovery': []
            }

    # Defines the boat data holder.
    boat_Data = Boat_Data()

    """
    This section very simply iterates through the supplied .txt file and constructs a 2D Array which makes searching the
    file for data much easier.
    """
    # Turning txt into grid format - Formats into a 2d list. (Row, Column)
    for line in file.stream:
        row = []
        decoded_line = line.decode("utf-8").replace("\r", "")
        line_list = decoded_line.split("	")

        for element in line_list:
            row.append(element)
        grid.append(row)

    """
    This section searches through the constructed grid to set pointers to idenfiers, This makes the process of finding
    unique and calculated data significantly easier down the line.
    """
    # Essential identifers for grid search.
    counter = 0
    Boat_Info_Line = 0
    Column_Name_Line = 0
    Data_Start_Line = 0
    Data_End_Line = 0
    Side_Start_Line = 0
    GPS_Start_Line = 0
    GPS_End_Line = 0
    Crew_Info_Line = 0
    Date_Line = 0
    Serial_Line = 0
    Big_Data_Start_Line = 0
    Big_Data_Finish_Line = len(grid) - 1
    Big_Data_Column_Line = 0
    # Iterates through the 2d grid to locate essential line numbers in the list.
    for row in grid:
        if len(row) > 0:
            if (row[0] == 'Side\n') or (row[0] == 'Side'):
                Side_Start_Line = counter + 1

        if len(row) > 1:
            if (row[1] == 'SwivelPower') and (Data_Start_Line == 0):
                Data_Start_Line = counter + 2
                Column_Name_Line = counter

            if (row[1] == 'Seats'):
                Boat_Info_Line = counter + 1

            if (counter == Boat_Info_Line) and (counter != 0):
                boat_Data.BoatName = row[0]
                boat_Data.Seats = row[1]
                boat_Data.boatType = row[3]

        if len(row) > 2:
            if (row[2] == 'Chanb007'):
                if Data_End_Line == 0:
                    Data_End_Line = counter - 2

            if (row[0] == 'Sweep Oar Inboard'):
                boat_Data.Inboard = row[1]

            if (row[0] == 'Sweep Oar Length'):
                boat_Data.OarLength = row[1]

            if (row[2] == '0x800A'):
                GPS_End_Line = counter
                
        if len(row) > 4:
            if (row[3] == 'Start Time'):
                Date_Line = counter + 1
            if (row[0]) == 'Lat':
                boat_Data.Latitude = grid[counter+1][0]
            if (row[1]) == 'Lon':
                boat_Data.Longitude = grid[counter+1][1]

        if len(row) > 7:
            if row[0] == 'Serial #':
                Serial_Line = counter + 1

        if len(row) > 10:
            if row[1] == 'GateAngle':
                Big_Data_Start_Line = counter + 2
                Big_Data_Column_Line = counter

        if len(row) > 10:
            if row[1] == 'Name':
                Crew_Info_Line = counter + 1

        if len(row) > 12:
            if row[1] == 'GPS X Lo':
                GPS_Start_Line = counter + 2

        if (counter == Date_Line) and (counter != 0):
            boat_Data.Date = row[3]
        
        if (counter == Serial_Line) and (counter != 0):
            boat_Data.Serial = row[0]

        counter += 1

    """
    This section below is arguable the most significant in the program, it is responsible for iterating through the masses of data
    recorded every 50ms from Peach Telemetry.
    """

    findColumn = Subroutines.find_Column_Position
    list_Seat_Number_Columns = []
    for i in grid[Big_Data_Column_Line+1]:
        list_Seat_Number_Columns.append(i)

    # Applying big data to rower profiles
    seat_Iteration = 0
    for seat_Number in range(0,int(boat_Data.Seats)):
        # Checks if the seat is valid and was plugged in.
        if not (str(seat_Number+1) in list_Seat_Number_Columns):
            continue

        recorded_Strokes = 0
        start_Of_Stroke_Line = Big_Data_Start_Line
        end_Of_Stroke_Line = 0
        seat_Data = Rower_Data()

        seat_Data.Seat = str(seat_Number + 1)

        # Load rower side data (Port/Stbd) into class.
        for row in range(Side_Start_Line, Side_Start_Line + int(boat_Data.Seats)):
            if grid[row][0] == str(seat_Number + 1):
                side = grid[row][1].replace('\n','')
                seat_Data.Side = side

        for row in range(Crew_Info_Line, Crew_Info_Line + int(boat_Data.Seats)):
            if grid[row][0] == str(seat_Number + 1):
                if grid[row][1] != '':
                    seat_Data.Name = grid[row][1]

        # Load rower data into class array.
        for line in range(Data_Start_Line, Data_End_Line):
            row = grid[line]
            value = row[findColumn('Rower Swivel Power', grid, Column_Name_Line) + seat_Number]
            if value != '':
                seat_Data.data['Rower Swivel Power'].append(float(value))


        # Search through each line in the big data.
        for row in range(Big_Data_Start_Line, Big_Data_Finish_Line):
            normalisedTime = float(grid[row][Subroutines.find_Column_Position('Normalized Time', grid, Big_Data_Column_Line)])
            calculated_Value = normalisedTime - float(grid[row+1][Subroutines.find_Column_Position('Normalized Time', grid, Big_Data_Column_Line)])

            # Checks if the value is the end of the stroke.
            if (calculated_Value > 90 and calculated_Value < 100):
                lines_In_Stroke = 0

                end_Of_Stroke_Line = row

                List_GateAngles = []
                List_GateForceX = []
                List_NormalizedTime = []
                List_GateAngleVel = []
                List_SeatPos = []
                List_SeatPosVel = []
                List_BodyArmsVel = []
                List_PercentOfArc = []
                List_PercentOfMaxForce = []

                List_GateAnglePercentage = []
                List_GateForcePercentage = []

                List_Acceleration = []
                List_RollAngles = []
                List_PitchAngles = []
                List_YawAngles = []

                angle_related_cSlip = 0      # Angle on same row as blade locked on (<30kg)
                angle_related_FSlip = 0      # Angle on same row as blade disconnected (>15kg)

                stroke_Start_Distance = float(grid[start_Of_Stroke_Line][findColumn('Distance', grid, Big_Data_Column_Line)])
                stroke_End_Distance = float(grid[end_Of_Stroke_Line][findColumn('Distance', grid, Big_Data_Column_Line)])
                stroke_Distance = stroke_End_Distance - stroke_Start_Distance

                blade_Locked = False
                blade_unLocked = False

                # Iterates through the rows in a single stroke.
                for line in range(start_Of_Stroke_Line, end_Of_Stroke_Line):
                    lines_In_Stroke += 1

                    """
                    Collects all data from columns in the text file, if there is an error with one of the values being
                    collected and converted to float. Then none of the values will be recorded to ensure all arrays
                    stay the same size.
                    """
                    try:
                        # Appends all gateAngle values to a list.
                        gate_Angle = float(grid[line][findColumn('GateAngle', grid, Big_Data_Column_Line) + seat_Iteration])
                        List_GateAngles.append(gate_Angle)

                        # Appends all gateForce values to a list.
                        gate_Force = float(grid[line][findColumn('GateForceX', grid, Big_Data_Column_Line) + seat_Iteration])
                        List_GateForceX.append(gate_Force)

                        # Appends all GateAngleVel values to a list
                        gate_Angle_Vel = float(grid[line][findColumn('GateAngleVel', grid, Big_Data_Column_Line) + seat_Iteration])
                        List_GateAngleVel.append(gate_Angle_Vel)
                    
                        # Checks if seat sensors are valid hardware in the boat data log.
                        try:
                            # Appends all SeatPos values to a list
                            seat_Pos = float(grid[line][findColumn('Seat Posn', grid, Big_Data_Column_Line) + seat_Iteration])
                            List_SeatPos.append(seat_Pos)

                            # Appends all SeatPosVel values to a list
                            seat_Pos_Vel = float(grid[line][findColumn('Seat Posn Vel', grid, Big_Data_Column_Line) + seat_Iteration])
                            List_SeatPosVel.append(seat_Pos_Vel)
                        except:
                            pass
                
                        # Appends all normalizedTime values to a list.
                        normalized_Time = float(grid[line][findColumn('Normalized Time', grid, Big_Data_Column_Line)])
                        List_NormalizedTime.append(normalized_Time)

                        # Gets the boats acceleration
                        acceleration = float(grid[line][findColumn('Accel', grid, Big_Data_Column_Line)])
                        List_Acceleration.append(acceleration)

                        # Gets the boats Roll, Pitch, Yaw
                        roll = float(grid[line][findColumn('Roll Angle', grid, Big_Data_Column_Line)])
                        pitch = float(grid[line][findColumn('Pitch Angle', grid, Big_Data_Column_Line)])
                        yaw = float(grid[line][findColumn('Yaw Angle', grid, Big_Data_Column_Line)])

                        List_RollAngles.append(roll)
                        List_PitchAngles.append(pitch)
                        List_YawAngles.append(yaw)
                    except:
                        pass

                # Checks if the stroke found is a full stroke. If a half stroke is found then it won't be recorded.
                if ((min(List_NormalizedTime)) < -40 and (max(List_NormalizedTime) > 40)):
                    # Calculates max and 70% of force.
                    angle_related_70_gForce = 0
                    angle_related_Max_gForce = 0 
                    angle_related_from70_gForce = 0
                    max_GateForceX = max(List_GateForceX)
                    max70_GateForceX = (max_GateForceX / 100) * 70
                    PercentageMax70 = getPercentage(max_GateForceX, max70_GateForceX)

                    # Getting angles for catch slip
                    iteration = 0
                    for gate_Force in List_GateForceX:
                        gate_Angle = List_GateAngles[iteration]
                        # Gets the first gate force value above 29 kg, then finds the related angle at this point of the drive.
                        if gate_Force >= 30 and not blade_Locked:
                            blade_Locked = True
                            angle_related_cSlip = gate_Angle

                        # Gets the first gate force value below 15 kg after the blade has been locked, then finds the related angle at this point of the drive.
                        if gate_Force < 15 and not blade_unLocked and blade_Locked:
                            blade_unLocked = True
                            angle_related_FSlip = gate_Angle
                        iteration += 1

                    # Calcualtes angles.
                    Catch = min(List_GateAngles)
                    Finish = max(List_GateAngles)
                    real_Finish = Finish - 1 # -1 is the pause bound. (+30)
                    real_Catch = Catch + 1 # +1 is the hang bound. (-55)
                    arcLength = abs(Catch) + Finish
                    catchSlip = abs(Catch) - abs(angle_related_cSlip)
                    finishSlip = Finish - angle_related_FSlip

                    for angle in List_GateAngles:
                        pofarc = ((angle - Catch) / arcLength) * 100 # Turn into % of cycle
                        List_PercentOfArc.append(pofarc)

                    for gateforce in List_GateForceX:
                        pofmaxf = (gateforce / max_GateForceX) * 100
                        List_PercentOfMaxForce.append(pofmaxf)

                    # Angles of % on recovery - This finds the angle related to the percentage of recovery.
                    angle_25_recovery = 0
                    angle_50_recovery = 0
                    angle_75_recovery = 0

                    # Finds angles for % of recovery, this is used in the syncronisation and ratios plot.
                    for angle in List_GateAngles:
                        if angle != Catch:
                            percent_Of_Angle = (((angle - Finish) / ((arcLength) * -1)) * 100)

                            if percent_Of_Angle <= 25:
                                angle_25_recovery = angle
                            
                            if percent_Of_Angle <= 50:
                                angle_50_recovery = angle

                            if percent_Of_Angle <= 75:
                                angle_75_recovery = angle 
                        else:
                            break
                    
                    # Calculate the distance handle traveled in meters.
                    Perimeter = (float(boat_Data.Inboard) * float(2.0)) * math.pi
                    percent_Of_Total = arcLength / 360
                    ArcDistance = ((percent_Of_Total * Perimeter) / 100)
                    force_Newtons = max_GateForceX * 9.81
                    work_Done = force_Newtons * ArcDistance

                    # Finds the angle related to the forces
                    found_max70 = False
                    found_max = False
                    count = 0
                    for force in List_GateForceX:
                        if force >= max70_GateForceX and not found_max70:
                            angle_related_70_gForce = List_GateAngles[count]
                            found_max70 = True
                        if force >= max_GateForceX and not found_max:
                            angle_related_Max_gForce = List_GateAngles[count]
                            found_max = True
                        if force >= max70_GateForceX and found_max70:
                            angle_related_from70_gForce = List_GateAngles[count]
                        count += 1

                    # Getting catch and finish force gradients
                    # Rise over Run
                    try:
                        catchForceGradient = (abs(angle_related_cSlip) - abs(angle_related_Max_gForce))
                        finishForceGradient = (abs(angle_related_from70_gForce) - angle_related_FSlip)
                    except:
                        catchForceGradient = 0
                        finishForceGradient = 0

                    # Finding the average gateforce and shape of power curve.
                    iteration = 0
                    found_Catch = False
                    drive_GateForceX = []
                    position_Of_CSlip = 0
                    position_Of_70MaxF = 0
                    position_Of_MaxF = 0
                    position_Of_From70MaxF = 0
                    position_Of_FSlip = 0

                    for force in List_GateForceX:
                        angle = List_GateAngles[iteration]
                        if angle <= Catch and not found_Catch:
                            found_Catch = True

                        if angle >= Catch and angle <= Finish and found_Catch:
                            percent_Of_Angle = (((angle + abs(Catch)) / arcLength) * 100)

                            if force < 0:
                                percent_Of_Max = 0
                            else:
                                percent_Of_Max = getPercentage(max_GateForceX, force)
                            
                            if angle == angle_related_cSlip:
                                position_Of_CSlip = percent_Of_Angle
                            elif angle == angle_related_70_gForce:
                                position_Of_70MaxF = percent_Of_Angle
                            elif angle == angle_related_Max_gForce:
                                position_Of_MaxF = percent_Of_Angle
                            elif angle == angle_related_from70_gForce:
                                position_Of_From70MaxF = percent_Of_Angle
                            elif angle == angle_related_FSlip:
                                position_Of_FSlip = percent_Of_Angle

                            List_GateForcePercentage.append(percent_Of_Max)
                            List_GateAnglePercentage.append(percent_Of_Angle)

                        if angle >= Catch and angle <= Finish and found_Catch and force > 0:
                            drive_GateForceX.append(force)

                        iteration += 1

                    Average_GateForceX = getAverage(drive_GateForceX)
                    AvgGateForce_MaxGateForce = getPercentage(max_GateForceX, Average_GateForceX)

                    # Stroke time
                    iteration = 0
                    found_Min = False
                    found_Max = False

                    recovery_Length_1 = 0
                    recovery_Length_2 = 0
                    recovery_Length_3 = 0
                    recovery_Length_4 = 0
                    hang_Angles_1 = 0
                    hang_Angles_2 = 0
                    catch_slip_Angles = 0
                    first_drive_Length = 0
                    second_drive_Length = 0
                    third_drive_Length = 0
                    fourth_dive_Length = 0
                    finish_slip_Angles = 0
                    pause_Angles1 = 0
                    pause_Angles2 = 0
                    recovery_Length_5 = 0
                    after_Recovery = False
                    after_Finish = False

                    # Number of ticks taken (50hz) to get to each stage of the stroke.
                    Ticks_To_25Recov = 0
                    Ticks_To_50Recov = 0
                    Ticks_To_75Recov = 0
                    Ticks_To_Hang = 0
                    Ticks_To_Min = 0
                    Ticks_to_Catch = 0
                    Ticks_To_Effective_Drive = 0
                    Ticks_to_70MaxF = 0
                    Ticks_to_MaxF = 0
                    Ticks_to_From70MaxF = 0
                    Ticks_To_FSlip = 0
                    Ticks_to_Finish = 0
                    Ticks_to_Max = 0
                    Ticks_To_Recovery = 0

                    # Calculates where each section of the stroke is in the recorded angles.
                    for angle in List_GateAngles:
                        iteration += 1
                        # First Recovery
                        if not after_Recovery:
                            if (angle > real_Catch):
                                if angle >= angle_25_recovery:
                                    Ticks_To_25Recov = iteration
                                    recovery_Length_1 += 1

                                elif angle >= angle_50_recovery:
                                    Ticks_To_50Recov = iteration
                                    recovery_Length_2 += 1

                                elif angle >= angle_75_recovery:
                                    Ticks_To_75Recov = iteration
                                    recovery_Length_3 += 1
                                else:
                                    recovery_Length_4 += 1
                            else:
                                after_Recovery = True
                                Ticks_To_Hang = iteration

                        # After hang found
                        if after_Recovery and not after_Finish:
                            # After catch - 1 found
                            if (angle <= real_Catch): # 1 each side of value
                                if angle == Catch:
                                    found_Min = True
                                if not found_Min:
                                    hang_Angles_1 += 1
                                else:
                                    if Ticks_To_Min == 0:
                                        Ticks_To_Min = iteration
                                    hang_Angles_2 += 1
                                    Ticks_to_Catch = iteration

                            # Catch Slip
                            if (angle < angle_related_cSlip) and (angle > real_Catch):
                                catch_slip_Angles += 1

                            # Drive
                            if (angle >= angle_related_cSlip) and (angle < angle_related_FSlip): # Angle is between drive and finish (excluding catch + 1 and finish -1 area)
                                if Ticks_To_Effective_Drive == 0:
                                    Ticks_To_Effective_Drive = iteration
                                
                                # This section is fucking killing my brain. - sort by 05/01/2025
                                # UPDATE: The issue was solved because i'm stupid and forgot that I was dividing the related_MAXF_gate_angle intead of raw_MAXF to get the 70Max...
                                if angle == angle_related_70_gForce:
                                    Ticks_to_70MaxF = iteration
                                
                                if angle <= angle_related_70_gForce:
                                    first_drive_Length += 1
                                
                                if angle <= angle_related_Max_gForce and angle > angle_related_70_gForce:
                                    second_drive_Length += 1
                                    if angle == angle_related_Max_gForce:
                                        Ticks_to_MaxF = iteration

                                if angle > angle_related_70_gForce and angle > angle_related_Max_gForce and angle <= angle_related_from70_gForce:
                                    third_drive_Length += 1

                                if angle > angle_related_from70_gForce:
                                    fourth_dive_Length += 1
                                    if Ticks_to_From70MaxF == 0:
                                        Ticks_to_From70MaxF = iteration

                            # Finish Slip
                            if (angle >= angle_related_FSlip):
                                if (angle == angle_related_FSlip):
                                    Ticks_To_FSlip = iteration

                                if (angle < real_Finish):
                                    finish_slip_Angles += 1
                                else:
                                    after_Finish = True
                                    Ticks_to_Finish = iteration

                        # After drive ends
                        if after_Finish:
                            # Pause
                            if (angle >= real_Finish): # 1 each side of value
                                if Ticks_to_Finish == 0:
                                    Ticks_to_Finish = iteration

                                if angle == Finish:
                                    found_Max = True
                                
                                if not found_Max:
                                    pause_Angles1 += 1
                                else:
                                    if Ticks_to_Max == 0:
                                        Ticks_to_Max = iteration
                                    pause_Angles2 += 1

                            # Second Recovery
                            if (angle < real_Finish):
                                recovery_Length_5 += 1
                                if Ticks_To_Recovery == 0:
                                    Ticks_To_Recovery = iteration

                    # Seat Sensor Data
                    seat_Length = None
                    catch_Factor = None
                    try:
                        # Seat Timing Bar Plot
                        BeforeSeat_Length = 0
                        SeatRecovery_Length = 0
                        Pause1_Length = 0
                        Pause2_Length = 0
                        Drive_Length = 0
                        SeatDone1_Length = 0
                        SeatDone2_Length = 0

                        found_Min = False
                        found_Max = False
                        after_Seat_Start = False
                        after_Recovery_Seat = False
                        after_Catch_Seat = False
                        after_Drive_Seat = False

                        cm_List = []
                        for pos in List_SeatPos:
                            cm_List.append(pos / 10)

                        min_Pos = min(cm_List)
                        max_Pos = max(cm_List)
                        seat_Length = max_Pos - min_Pos

                        # Get the catch factor (difference in time between the seat and handle changing direction)
                        # CF = Time when seat velocity crosses zero - Time when handle velocity crosses zero
                        iteration = 0
                        seat_Change = 0
                        handle_Change = 0
                        found_Seat = False
                        found_Handle = False
                        for vel in List_SeatPosVel:
                            if not found_Seat:
                                if vel <= 0.0:
                                    seat_Change = iteration
                                    found_Seat = True
                            if not found_Handle:
                                if List_GateAngleVel[iteration] >= 0.0:
                                    handle_Change = iteration
                                    found_Handle = True
                            iteration += 1
                        catch_Factor = (seat_Change / 50) - (handle_Change / 50)

                        # Body Arms Velocity calculation
                        count = 0
                        for gate_angle_velocity in List_GateAngleVel:
                            gate_angle = List_GateAngles[count]
                            seat_position_velocity = List_SeatPosVel[count]
                            
                            inboard = 1.14
                            #linear_handle_vel = ((gate_angle_velocity * (math.pi() / 180)) * inboard)
                            linear_handle_vel = ((gate_angle_velocity * 19.2) * math.cos(math.radians(gate_angle)))
                            body_arms_vel = linear_handle_vel - seat_position_velocity
                            List_BodyArmsVel.append(body_arms_vel)
                            count += 1

                        for pos in cm_List:
                            # Before Seat Recovery
                            if (pos >= (max_Pos - 1)) and (not after_Seat_Start):
                                BeforeSeat_Length += 1

                            # During Seat Recovery
                            elif (pos <= (max_Pos - 1)) and (pos >= min_Pos + 1) and (not after_Recovery_Seat):
                                after_Seat_Start = True
                                SeatRecovery_Length += 1

                            # Front End Pause
                            elif (pos <= (min_Pos + 1)) and (not after_Catch_Seat):
                                after_Recovery_Seat = True
                                if (pos > min_Pos) and (not found_Min):
                                    Pause1_Length += 1
                                else:
                                    found_Min = True
                                    Pause2_Length += 1

                            # Seat Drive Phase
                            elif ((pos >= (min_Pos + 1)) and (pos <= (max_Pos - 1))):
                                after_Catch_Seat = True
                                Drive_Length += 1

                            # Seat Stationary Phase
                            elif (pos >= (max_Pos - 1)):
                                if (pos < max_Pos) and (not after_Drive_Seat):
                                    SeatDone1_Length += 1
                                else:
                                    after_Drive_Seat = True
                                    SeatDone2_Length += 1
                    except:
                        pass

                    # Stroke segment timing data.
                    stroke_Time = float(lines_In_Stroke / 50)
                    
                    recovery_Time1 = float(recovery_Length_1 / 50) * 1000
                    recovery_Time2 = float(recovery_Length_2 / 50) * 1000
                    recovery_Time3 = float(recovery_Length_3 / 50) * 1000
                    recovery_Time4 = float(recovery_Length_4 / 50) * 1000
                    hang_Time1 = float(hang_Angles_1 / 50) * 1000
                    hang_Time2 = float(hang_Angles_2 / 50) * 1000
                    c_Slip_Time = float(catch_slip_Angles / 50) * 1000
                    drive_Time1 = float(first_drive_Length / 50) * 1000
                    drive_Time2 = float(second_drive_Length / 50) * 1000
                    drive_Time3 = float(third_drive_Length / 50) * 1000
                    drive_Time4 = float(fourth_dive_Length / 50) * 1000
                    f_Slip_Time = float(finish_slip_Angles / 50) * 1000
                    pause_Time1 = float(pause_Angles1 / 50) * 1000
                    pause_Time2 = float(pause_Angles2 / 50) * 1000
                    recovery_Time5 = float(recovery_Length_5 / 50) * 1000
                    total_Drive_Time = (drive_Time1 + drive_Time2 + drive_Time3 + drive_Time4 + c_Slip_Time + f_Slip_Time + pause_Time1) / 1000
                    total_Recovery_Time = (recovery_Time1 + recovery_Time2 + recovery_Time3 + recovery_Time4 + pause_Time2 + hang_Time1) / 1000

                    # Seat segment timing data
                    before_Seat_Time = float(BeforeSeat_Length / 50)
                    seat_Recovery_Time = float(SeatRecovery_Length / 50)
                    Pause1_Time = float(Pause1_Length / 50)
                    Pause2_Time = float(Pause2_Length / 50)
                    Drive_Time = float(Drive_Length / 50)
                    SeatDone1_Time = float(SeatDone1_Length / 50)
                    SeatDone2_Time = float(SeatDone2_Length / 50)

                    # Syncronisation data.
                    Time_To_25_Recov = (Ticks_To_25Recov / 50) * 1000
                    Time_To_50_Recov = (Ticks_To_50Recov / 50) * 1000
                    Time_To_75_Recov = (Ticks_To_75Recov / 50) * 1000
                    Time_To_Hang = (Ticks_To_Hang / 50) * 1000
                    Time_To_Min = (Ticks_To_Min / 50) * 1000
                    Time_To_Catch = (Ticks_to_Catch / 50) * 1000
                    Time_To_Effective_Start = (Ticks_To_Effective_Drive / 50) * 1000
                    Time_To_70MaxF = (Ticks_to_70MaxF / 50) * 1000
                    Time_To_MaxF = (Ticks_to_MaxF / 50) * 1000
                    Time_To_From70Maxf = (Ticks_to_From70MaxF / 50) * 1000
                    Time_To_Effective_End = (Ticks_To_FSlip / 50) * 1000
                    Time_To_Finish = (Ticks_to_Finish / 50) * 1000
                    Time_To_Max = (Ticks_to_Max / 50) * 1000
                    Time_To_Recovery = (Ticks_To_Recovery / 50) * 1000

                    stroke_Rate = (60 / stroke_Time)

                    # Append to the rowers individual data.
                    recorded_Strokes += 1

                    # Store data into class
                    data_container = seat_Data.data
                    data_container['Stroke Time'].append(stroke_Time)
                    data_container['Recovery Time 1'].append(recovery_Time1)
                    data_container['Recovery Time 2'].append(recovery_Time2)
                    data_container['Recovery Time 3'].append(recovery_Time3)
                    data_container['Recovery Time 4'].append(recovery_Time4)
                    data_container['Hang Time 1'].append(hang_Time1)
                    data_container['Hang Time 2'].append(hang_Time2)
                    data_container['Catch Slip Time'].append(c_Slip_Time)
                    data_container['Drive Time 1'].append(drive_Time1)
                    data_container['Drive Time 2'].append(drive_Time2)
                    data_container['Drive Time 3'].append(drive_Time3)
                    data_container['Drive Time 4'].append(drive_Time4)
                    data_container['Finish Slip Time'].append(f_Slip_Time)
                    data_container['Pause Time 1'].append(pause_Time1)
                    data_container['Pause Time 2'].append(pause_Time2)
                    data_container['Recovery Time 5'].append(recovery_Time5)
                    data_container['Total Drive Time'].append(total_Drive_Time)
                    data_container['Total Recovery Time'].append(total_Recovery_Time)

                    data_container['Before Seat'].append(before_Seat_Time)
                    data_container['Seat Recovery'].append(seat_Recovery_Time)
                    data_container['Pause 1'].append(Pause1_Time)
                    data_container['Pause 2'].append(Pause2_Time)
                    data_container['Drive'].append(Drive_Time)
                    data_container['Drive Finished 1'].append(SeatDone1_Time)
                    data_container['Drive Finished 2'].append(SeatDone2_Time)

                    data_container['Work Per Stroke'].append(work_Done)
                    data_container['GateForceX'].append(List_GateForceX)
                    data_container['70MaxGateForceX'].append(max70_GateForceX)
                    data_container['MaxGateForceX'].append(max_GateForceX)
                    data_container['AvgGateForceX'].append(Average_GateForceX)
                    data_container['Average Force / Max Force'].append(AvgGateForce_MaxGateForce)
                    data_container['Angle_70MaxGateForceX'].append(angle_related_70_gForce)
                    data_container['Angle_MaxGateForceX'].append(angle_related_Max_gForce)
                    data_container['Angle_From70MaxGateForceX'].append(angle_related_from70_gForce)
                    data_container['Normalized Time'].append(List_NormalizedTime)
                    data_container['GateAngleVel'].append(List_GateAngleVel)
                    data_container['PercentageForce'].append(List_GateForcePercentage)
                    data_container['PercentageAngle'].append(List_GateAnglePercentage)
                    data_container['Percentage70%MaxForce'].append(PercentageMax70)

                    data_container['GateAngle'].append(List_GateAngles)
                    data_container['ArcLength'].append(arcLength)
                    data_container['Effective Length'].append(arcLength - catchSlip - finishSlip)
                    data_container['MaxAngle'].append(Finish)
                    data_container['MinAngle'].append(Catch)
                    data_container['Effective MinAngle'].append(angle_related_cSlip)
                    data_container['Effective MaxAngle'].append(angle_related_FSlip)
                    data_container['CatchSlip'].append(catchSlip)
                    data_container['FinishSlip'].append(finishSlip)
                    data_container['Catch Force Gradient'].append(catchForceGradient)
                    data_container['Finish Force Gradient'].append(finishForceGradient)
                    data_container['Catch Factor'].append(catch_Factor)
                    data_container['PercentOfArc'].append(List_PercentOfArc)
                    data_container['PercentOfMaxForce'].append(List_PercentOfMaxForce)

                    # Seat Data
                    data_container['SeatPosn'].append(List_SeatPos)
                    data_container['SeatPosnVel'].append(List_SeatPosVel)
                    data_container['SeatLength'].append(seat_Length)
                    data_container['BodyArmsVel'].append(List_BodyArmsVel)
                    try:
                        data_container['SeatMaxVel'].append((max(List_SeatPosVel) / 1000)) # converts mm/s to m/s
                    except:
                        data_container['SeatMaxVel'].append(None)
                        boat_Data.SeatSensors = False


                    data_container['Position_Of_CSlip'].append(position_Of_CSlip)
                    data_container['Position_Of_70MaxF'].append(position_Of_70MaxF)
                    data_container['Position_Of_MaxF'].append(position_Of_MaxF)
                    data_container['Position_Of_From70MaxF'].append(position_Of_From70MaxF)
                    data_container['Posititon_Of_FSlip'].append(position_Of_FSlip)

                    data_container['Time_To_25%'].append(Time_To_25_Recov)
                    data_container['Time_To_50%'].append(Time_To_50_Recov)
                    data_container['Time_To_75%'].append(Time_To_75_Recov)
                    data_container['Time_To_Hang'].append(Time_To_Hang)
                    data_container['Time_To_Min'].append(Time_To_Min)
                    data_container['Time_To_Catch'].append(Time_To_Catch)
                    data_container['Time_To_Effective_Start'].append(Time_To_Effective_Start)
                    data_container['Time_To_70Max'].append(Time_To_70MaxF)
                    data_container['Time_To_MaxF'].append(Time_To_MaxF)
                    data_container['Time_To_From70Max'].append(Time_To_From70Maxf)
                    data_container['Time_To_Effective_End'].append(Time_To_Effective_End)
                    data_container['Time_To_Finish'].append(Time_To_Finish)
                    data_container['Time_To_Max'].append(Time_To_Max)
                    data_container['Time_To_Recovery'].append(Time_To_Recovery)

                    if seat_Number == 0:
                        boat_Data.data['Distance / Stroke'].append(stroke_Distance)
                        boat_Data.data['Stroke Time'].append(stroke_Time)
                        boat_Data.data['Acceleration'].append(List_Acceleration)
                        boat_Data.data['Meters/s'].append(stroke_Distance / stroke_Time)
                        boat_Data.data['RollAngle'].append(List_RollAngles)
                        boat_Data.data['PitchAngle'].append(List_PitchAngles)
                        boat_Data.data['YawAngle'].append(List_YawAngles)
                        boat_Data.data['Rating'].append(stroke_Rate)
                        boat_Data.data['Normalized Time'].append(List_NormalizedTime)


                # Sets the pointer to the next stroke start line.
                start_Of_Stroke_Line = row + 1

        seat_Data.Recorded_Strokes = recorded_Strokes
        profiles_List.append(seat_Data)
        seat_Iteration += 1

    """
    This section is responsible for asigning the boat data into it's idenfier which contains a cloned class.
    """
    # Appending to boat data
    iteration = 0
    for i in range(Data_Start_Line, Data_End_Line):
        Average_Power = grid[i][Subroutines.find_Column_Position('Average Power', grid, Column_Name_Line)]

        if Average_Power != '':
            if (not (iteration in strokes_Skipped)):
                boat_Data.data['Average Power'].append(Average_Power)
        
            iteration += 1

    start_Distance = grid[Big_Data_Start_Line][Subroutines.find_Column_Position('Distance', grid, Big_Data_Column_Line)]
    end_Distance = grid[Big_Data_Finish_Line][Subroutines.find_Column_Position('Distance', grid, Big_Data_Column_Line)]
    piece_Distance = float(end_Distance) - float(start_Distance)

    total_Counted_Strokes = 0
    for rower in profiles_List:
        total_Counted_Strokes += rower.Recorded_Strokes

    total_Strokes = total_Counted_Strokes / int(boat_Data.Seats)
    time = float(Subroutines.get_Sum(boat_Data.data['Stroke Time']))

    boat_Data.tStrokes = (total_Strokes)
    boat_Data.timeElapsed = (time)
    boat_Data.Distance = (piece_Distance)

    """
    GPS Section
    """
    for row in range(GPS_Start_Line, GPS_End_Line):
        latitude = float(grid[row][11])
        longitude = float(grid[row][12])
        array = [latitude, longitude]
        boat_Data.data['GPS'].append(array)

    # Setting syncronisation
    Stroke_25_Recov = []
    Stroke_50_Recov = []
    Stroke_75_Recov = []
    Stroke_Hang = []
    Stroke_Min = []
    Stroke_Catch = []
    Stroke_Effective_Drive = []
    Stroke_70Max_F = []
    Stroke_MaxF = []
    Stroke_From70Max_F = []
    Stroke_FSlip = []
    Stroke_Finish = []
    Stroke_Max = []
    Stroke_Recovery = []

    stroke_Seat = profiles_List[-1]
    for count in range(0, len(stroke_Seat.data['Time_To_25%'])):
        Stroke_25_Recov.append(stroke_Seat.data['Time_To_25%'][count])
        Stroke_50_Recov.append(stroke_Seat.data['Time_To_50%'][count])
        Stroke_75_Recov.append(stroke_Seat.data['Time_To_75%'][count])
        Stroke_Hang.append(stroke_Seat.data['Time_To_Hang'][count])
        Stroke_Min.append(stroke_Seat.data['Time_To_Min'][count])
        Stroke_Catch.append(stroke_Seat.data['Time_To_Catch'][count])
        Stroke_Effective_Drive.append(stroke_Seat.data['Time_To_Effective_Start'][count])
        Stroke_70Max_F.append(stroke_Seat.data['Time_To_70Max'][count])
        Stroke_MaxF.append(stroke_Seat.data['Time_To_Max'][count])
        Stroke_From70Max_F.append(stroke_Seat.data['Time_To_From70Max'][count])
        Stroke_FSlip.append(stroke_Seat.data['Time_To_Effective_End'][count])
        Stroke_Finish.append(stroke_Seat.data['Time_To_Finish'][count])
        Stroke_Max.append(stroke_Seat.data['Time_To_Max'][count])
        Stroke_Recovery.append(stroke_Seat.data['Time_To_Recovery'][count])

    for rower in profiles_List:
        for count in range(0, len(stroke_Seat.data['Time_To_25%'])):
            Recov_25_Time = rower.data['Time_To_25%'][count]
            Recov_50_Time = rower.data['Time_To_50%'][count]
            Recov_75_Time = rower.data['Time_To_75%'][count]
            Hang_Time = rower.data['Time_To_Hang'][count]
            Min_Time = rower.data['Time_To_Min'][count]
            Catch_Time = rower.data['Time_To_Catch'][count]
            Effective_Drive_Time = rower.data['Time_To_Effective_Start'][count]
            MaxF70_Time = rower.data['Time_To_70Max'][count]
            MaxF_Time = rower.data['Time_To_Max'][count]
            MaxFrom70_Time = rower.data['Time_To_From70Max'][count]
            FSlip_Time = rower.data['Time_To_Effective_End'][count]
            Finish_Time = rower.data['Time_To_Finish'][count]
            Max_Time = rower.data['Time_To_Max'][count]
            Recovery_Time = rower.data['Time_To_Recovery'][count]

            Recov_25_Difference = round((Recov_25_Time-Stroke_25_Recov[count]),3)
            Recov_50_Difference = round((Recov_50_Time-Stroke_50_Recov[count]),3)
            Recov_75_Difference = round((Recov_75_Time-Stroke_75_Recov[count]),3)
            Hang_Difference = round((Hang_Time-Stroke_Hang[count]),3)
            Min_Difference = round((Min_Time-Stroke_Min[count]),3)
            Catch_Difference = round((Catch_Time-Stroke_Catch[count]),3)
            Effective_Drive_Difference = round((Effective_Drive_Time-Stroke_Effective_Drive[count]),3)
            MaxF70_Difference = round((MaxF70_Time-Stroke_70Max_F[count]),3)
            MaxF_Difference = round((MaxF_Time-Stroke_MaxF[count]),3)
            MaxFrom70_Difference = round((MaxFrom70_Time-Stroke_From70Max_F[count]),3)
            FSlip_Difference = round((FSlip_Time-Stroke_FSlip[count]),3)
            Finish_Difference = round((Finish_Time-Stroke_Finish[count]),3)
            Max_Difference = round((Max_Time-Stroke_Max[count]),3)
            Recovery_Difference = round((Recovery_Time-Stroke_Recovery[count]),3)

            rower.data['Difference_25'].append(Recov_25_Difference)
            rower.data['Difference_50'].append(Recov_50_Difference)
            rower.data['Difference_75'].append(Recov_75_Difference)
            rower.data['Difference_Hang'].append(Hang_Difference)
            rower.data['Difference_Min'].append(Min_Difference)
            rower.data['Difference_Catch'].append(Catch_Difference)
            rower.data['Difference_Effective_Start'].append(Effective_Drive_Difference)
            rower.data['Difference_70Max'].append(MaxF70_Difference)
            rower.data['Difference_MaxF'].append(MaxF_Difference)
            rower.data['Difference_Max70'].append(MaxFrom70_Difference)
            rower.data['Difference_Effective_End'].append(FSlip_Difference)
            rower.data['Difference_Finish'].append(Finish_Difference)
            rower.data['Difference_Max'].append(Max_Difference)
            rower.data['Difference_Recovery'].append(Recovery_Difference)

    # Data is returned to upload_file.py
    return profiles_List, boat_Data