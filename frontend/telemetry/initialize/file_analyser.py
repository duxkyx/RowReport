# Peach Telemetry data analysis program | Developed by Ben Loggie
# This program file will take the found file and convert it into a grid format, this grid is then searched and calculations are made to find the relevent data.

import telemetry.modules.maths as maths_module
import telemetry.initialize.temp_classes as temp_classes
import telemetry.initialize.file_analyser_modules.file_stream as file_stream
import math

def get_session_data(file):
    # List of athlete data holding 8x objects to be returned.
    profiles_List = []

    # Variable if the session has seat sensors.
    session_SeatSensors = False

    # Calculation required functions.
    getPercentage = maths_module.calculate_Percentage
    getAverage = maths_module.calculate_Average
    calculate_time = maths_module.calculate_time
    iterRows = file_stream.iterate_rows

    # Defines the boat data holder.
    boat_Data = temp_classes.Boat_Data()
    boat_Data.FileName = file.filename

    # Get the line numbers for data.
    layout = file_stream.scan_file_layout(file)
    Big_Data_Start_Line  = layout["Big_Data_Start_Line"]
    Regular_Data_Start_Line = layout['Data_Start_Line']
    Regular_Data_Finish_Line = layout['Data_End_Line']
    Side_Start_Line = layout['Side_Start_Line']
    Crew_Info_Line = layout['Crew_Info_Line']

    # Define boat data returned from streamed file.
    boat_Data.Seats = layout['Seats']
    boat_Data.Latitude = layout['Lat']
    boat_Data.Longitude = layout['Lon']
    boat_Data.boatType = layout['RowingType']
    boat_Data.Date = layout['Date']

    # Column cache.
    def get_Column_Pos(headers, expected):
        position = 0
        for i in headers:
            if i == expected:
                return position
            else:
                position += 1
        return False

    column_cache = {}

    REGULAR_COLUMNS = {"Rower Swivel Power", "Average Power"}
    def column(name):
        if name not in column_cache:
            if name in REGULAR_COLUMNS:
                column_cache[name] = get_Column_Pos(layout['Regular_Data_Headers'], name)
            else:
                column_cache[name] = get_Column_Pos(layout['Big_Data_Headers'], name)
        return column_cache[name]
    
    # Seat sides and names
    seat_side_map = {}
    seat_name_map = {}

    file.stream.seek(0)
    for i, row in enumerate(iterRows(file)):
        if Side_Start_Line <= i < Side_Start_Line + boat_Data.Seats:
            seat_side_map[row[0]] = row[1].strip()

        if Crew_Info_Line <= i < Crew_Info_Line + boat_Data.Seats:
            if row[1]:
                seat_name_map[row[0]] = row[1]


    # Iterating through seats to retreiving data from file.
    for seat_Number in range(boat_Data.Seats):
        recorded_Strokes = 0

        # Setup dat storage object.
        seat_Data = temp_classes.Rower_Data()
        seat_Data.Seat = str(seat_Number + 1)

        # Load athlete Name and Side into object attribute.
        seat_Data.Side = seat_side_map.get(seat_Data.Seat)
        seat_Data.Name = seat_name_map.get(seat_Data.Seat)

        # Rower swivel power
        file.stream.seek(0)
        for i, row in enumerate(iterRows(file)):

            if i < Regular_Data_Start_Line:
                continue
            if i > Regular_Data_Finish_Line:
                break

            value = row[column('Rower Swivel Power') + seat_Number]
            if value:
                seat_Data.data['Rower Swivel Power'].append(float(value))

        prev_row = None
        current_stroke_rows = []

        # Search through the entire file.
        file.stream.seek(0) 
        for i, row in enumerate(iterRows(file)):

            # Skip until Big Data starts
            if i < Big_Data_Start_Line:
                continue

            if prev_row is None:
                prev_row = row
                continue

            # Stroke boundary detection
            prev_norm = float(prev_row[column('Normalized Time')])
            curr_norm = float(row[column('Normalized Time')])
            delta = prev_norm - curr_norm

            current_stroke_rows.append(prev_row)

            # Checks if the value is the end of the stroke.
            if (90 < delta < 100):
                List_GateAngles = []
                List_GateForceX = []
                List_NormalizedTime = []
                List_GateAngleVel = []
                List_SeatPos = []
                List_SeatPosVel = []
                List_BodyArmsVel = []

                List_GateAnglePercentage = []
                List_GateForcePercentage = []

                List_Acceleration = []
                List_RollAngles = []
                List_PitchAngles = []
                List_YawAngles = []

                stroke_Start_Distance = float(current_stroke_rows[0][column('Distance')])
                stroke_End_Distance = float(current_stroke_rows[-1][column('Distance')])
                stroke_Distance = stroke_End_Distance - stroke_Start_Distance

                blade_Locked = False
                blade_unLocked = False

                seat_Sensors = False
                error = False

                # Iterates through the rows in a single stroke.
                for stroke_row in current_stroke_rows:
                    try:
                        # Appends all gateAngle values to a list.
                        gate_Angle = stroke_row[column('GateAngle') + seat_Number]
                        List_GateAngles.append(float(gate_Angle))

                        # Appends all gateForce values to a list.
                        gate_Force = stroke_row[column('GateForceX') + seat_Number]
                        List_GateForceX.append(float(gate_Force))

                        # Appends all GateAngleVel values to a list
                        gate_Angle_Vel = float(stroke_row[column('GateAngleVel') + seat_Number])
                        List_GateAngleVel.append(gate_Angle_Vel)
                    
                        # Checks if seat sensors are valid hardware in the boat data log.
                        try:
                            # Appends all SeatPos values to a list
                            seat_Pos = float(stroke_row[column('Seat Posn') + seat_Number])
                            List_SeatPos.append(seat_Pos)

                            # Appends all SeatPosVel values to a list
                            seat_Pos_Vel = float(stroke_row[column('Seat Posn Vel') + seat_Number])
                            List_SeatPosVel.append(seat_Pos_Vel)
                            seat_Sensors = True
                            session_SeatSensors = True
                        except:
                            seat_Sensors = False

                        # Appends all normalizedTime values to a list.
                        normalized_Time = float(stroke_row[column('Normalized Time')])
                        List_NormalizedTime.append(normalized_Time)

                        # Gets the boats acceleration
                        acceleration = float(stroke_row[column('Accel')])
                        List_Acceleration.append(acceleration)

                        # Gets the boats Roll, Pitch, Yaw
                        roll = float(stroke_row[column('Roll Angle')])
                        pitch = float(stroke_row[column('Pitch Angle')])
                        yaw = float(stroke_row[column('Yaw Angle')])

                        List_RollAngles.append(roll)
                        List_PitchAngles.append(pitch)
                        List_YawAngles.append(yaw)
                    except:
                        error = True
                        continue

                # Checks if the stroke found is a full stroke. If a half stroke is found then it won't be recorded.
                if (error == False) and ((min(List_NormalizedTime)) < -40 and (max(List_NormalizedTime) > 40)):

                    # Define variables for calculations
                    angle_related_cSlip = 0      # Angle on same row as blade locked on (<30kg)
                    angle_related_FSlip = 0      # Angle on same row as blade disconnected (>15kg)

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

                    # Angles of % on recovery - This finds the angle related to the percentage of recovery.
                    angle_25_recovery = 0
                    angle_50_recovery = 0
                    angle_75_recovery = 0

                    # Finds angles for % of recovery, this is used in the syncronisation and ratios plot.
                    iteration = 0
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
                        iteration += 1

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
                        catchForceGradient = (abs(Catch) - abs(angle_related_70_gForce))
                        finishForceGradient = (abs(angle_related_from70_gForce) - Finish)
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

                    if seat_Sensors:
                        max_Pos = max(List_SeatPos) / 10
                        min_Pos = min(List_SeatPos) / 10

                    found_Min = False
                    found_Max = False

                    # Calculates where each section of the stroke is in the recorded angles.
                    for angle in List_GateAngles:
                        iteration += 1

                        # First Recovery
                        if not after_Recovery:
                            if (angle > real_Catch):
                                if angle >= angle_25_recovery:
                                    recovery_Length_1 += 1

                                elif angle >= angle_50_recovery:
                                    if Ticks_To_25Recov == 0:
                                        Ticks_To_25Recov = iteration

                                    recovery_Length_2 += 1

                                elif angle >= angle_75_recovery:
                                    if Ticks_To_50Recov == 0:
                                        Ticks_To_50Recov = iteration

                                    recovery_Length_3 += 1
                                else:
                                    if Ticks_To_75Recov == 0:
                                        Ticks_To_75Recov = iteration
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
                            # Angle is between drive and finish (excluding catch + 1 and finish -1 area)
                            if (angle >= angle_related_cSlip) and (angle < angle_related_FSlip): 
                                if Ticks_To_Effective_Drive == 0:
                                    Ticks_To_Effective_Drive = iteration
                                
                                # This section is killing my brain. - sort by 05/01/2025
                                # UPDATE: The issue was solved because i'm stupid and forgot
                                # that I was dividing the related_MAXF_gate_angle intead of raw_MAXF to get the 70Max...
                                if angle == angle_related_70_gForce:
                                    if Ticks_to_70MaxF == 0:
                                        Ticks_to_70MaxF = iteration
                                
                                if angle <= angle_related_70_gForce:
                                    first_drive_Length += 1
                                
                                if angle <= angle_related_Max_gForce and angle > angle_related_70_gForce:
                                    second_drive_Length += 1
                                    if angle == angle_related_Max_gForce:
                                        if Ticks_to_MaxF == 0:
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
                                    if Ticks_To_FSlip == 0:
                                        Ticks_To_FSlip = iteration

                                if (angle < real_Finish):
                                    finish_slip_Angles += 1
                                else:
                                    after_Finish = True
                                    if Ticks_to_Finish == 0:
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
                        # Seat Length calculation
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
                        reached_Min_SeatPos = False
                        reached_Min_Angle = False
                        for pos in List_SeatPos:
                            GateAngle = List_GateAngles[iteration]

                            if not reached_Min_SeatPos:
                                if pos == min(List_SeatPos):
                                    reached_Min_SeatPos = True
                            else:
                                if pos > min(List_SeatPosVel) and seat_Change == 0:
                                    seat_Change = iteration

                            if not reached_Min_Angle:
                                if GateAngle == min(List_GateAngles):
                                    reached_Min_Angle = True
                            else:
                                if GateAngle >= min(List_GateAngles) and handle_Change == 0:
                                    handle_Change = iteration

                            iteration += 1

                        catch_Factor = calculate_time(seat_Change) - calculate_time(handle_Change)

                        # Body Arms Velocity calculation
                        count = 0
                        for gate_angle_velocity in List_GateAngleVel:
                            gate_angle = List_GateAngles[count]
                            seat_position_velocity = List_SeatPosVel[count]

                            linear_handle_vel = ((gate_angle_velocity * 19.2) * math.cos(math.radians(gate_angle)))

                            body_arms_vel = linear_handle_vel - seat_position_velocity
                            List_BodyArmsVel.append(body_arms_vel)
                            count += 1
                    except:
                        pass

                    # Stroke segment timing data.
                    stroke_Time = calculate_time(len(List_GateAngles)) / 1000

                    recovery_Time1 = calculate_time(recovery_Length_1)
                    recovery_Time2 = calculate_time(recovery_Length_2)
                    recovery_Time3 = calculate_time(recovery_Length_3)
                    recovery_Time4 = calculate_time(recovery_Length_4)
                    hang_Time1 = calculate_time(hang_Angles_1)
                    hang_Time2 = calculate_time(hang_Angles_2)
                    c_Slip_Time = calculate_time(catch_slip_Angles)
                    drive_Time1 = calculate_time(first_drive_Length)
                    drive_Time2 = calculate_time(second_drive_Length)
                    drive_Time3 = calculate_time(third_drive_Length)
                    drive_Time4 = calculate_time(fourth_dive_Length)
                    f_Slip_Time = calculate_time(finish_slip_Angles)
                    pause_Time1 = calculate_time(pause_Angles1)
                    pause_Time2 = calculate_time(pause_Angles2)
                    recovery_Time5 = calculate_time(recovery_Length_5)
                    total_Drive_Time = (drive_Time1 + drive_Time2 + drive_Time3 + drive_Time4 + c_Slip_Time + f_Slip_Time) / 1000
                    total_Recovery_Time = (recovery_Time1 + recovery_Time2 + recovery_Time3 + recovery_Time4 + pause_Time1 + pause_Time2 + hang_Time1 + hang_Time2 + recovery_Time5) / 1000

                    # Syncronisation data.
                    Time_To_25_Recov = calculate_time(Ticks_To_25Recov)
                    Time_To_50_Recov = calculate_time(Ticks_To_50Recov)
                    Time_To_75_Recov = calculate_time(Ticks_To_75Recov)
                    Time_To_Hang = calculate_time(Ticks_To_Hang)
                    Time_To_Min = calculate_time(Ticks_To_Min)
                    Time_To_Catch = calculate_time(Ticks_to_Catch)
                    Time_To_Effective_Start = calculate_time(Ticks_To_Effective_Drive)
                    Time_To_70MaxF = calculate_time(Ticks_to_70MaxF)
                    Time_To_MaxF = calculate_time(Ticks_to_MaxF)
                    Time_To_From70Maxf = calculate_time(Ticks_to_From70MaxF)
                    Time_To_Effective_End = calculate_time(Ticks_To_FSlip)
                    Time_To_Finish = calculate_time(Ticks_to_Finish)
                    Time_To_Max = calculate_time(Ticks_to_Max)
                    Time_To_Recovery = calculate_time(Ticks_To_Recovery)

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

                    # Seat Data
                    if seat_Sensors:
                        data_container['Catch Factor'].append(catch_Factor)
                        data_container['SeatLength'].append(seat_Length)
                        data_container['SeatMaxVel'].append((max(List_SeatPosVel) / 1000)) # converts mm/s to m/s
                        data_container['BodyArmsVel'].append(List_BodyArmsVel)
                        data_container['SeatPosn'].append(List_SeatPos)
                        data_container['SeatPosnVel'].append(List_SeatPosVel)
                    else:
                        same_length_list_holder = []
                        for i in List_GateAngleVel:
                            same_length_list_holder.append(1)
                        data_container['SeatPosn'].append(same_length_list_holder)
                        data_container['SeatPosnVel'].append(same_length_list_holder)
                        data_container['BodyArmsVel'].append(same_length_list_holder)

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

                        catch_NormalizedPosition = List_NormalizedTime[List_GateAngles.index(min(List_GateAngles))]
                        finish_NormalizedPosition = List_NormalizedTime[List_GateAngles.index(max(List_GateAngles))]

                        boat_Data.data['CatchNormalized'].append(catch_NormalizedPosition)
                        boat_Data.data['FinishNormalized'].append(finish_NormalizedPosition)
                        boat_Data.SeatSensors = session_SeatSensors

                current_stroke_rows = []
            prev_row = row

        # After the entire file has been streamed through.
        seat_Data.Recorded_Strokes = recorded_Strokes
        profiles_List.append(seat_Data)

    """
    This section is responsible for asigning the boat data from the raw text file into the boat data class.
    Boat Data Assignment
    """
    # Appending to boat data
    file.stream.seek(0) 
    for i, row in enumerate(iterRows(file)):
        if i < layout['Data_Start_Line']:
            continue
        if i >= layout['Data_End_Line']:
            break

        Average_Power = row[column('Average Power')]

        if Average_Power != '':
            boat_Data.data['Average Power'].append(float(Average_Power))

    start_Distance = 0
    end_Distance = 0
    file.stream.seek(0) 
    for i, row in enumerate(iterRows(file)):
        if i < layout['Big_Data_Start_Line']:
            continue

        if start_Distance == 0:
            start_Distance = row[column('Distance')]

        end_Distance = row[column('Distance')]

    piece_Distance = float(end_Distance) - float(start_Distance)

    total_Counted_Strokes = 0
    for rower in profiles_List:
        total_Counted_Strokes += rower.Recorded_Strokes

    total_Strokes = total_Counted_Strokes / int(boat_Data.Seats)
    time = float(maths_module.get_Sum(boat_Data.data['Stroke Time']))

    boat_Data.tStrokes = (total_Strokes)
    boat_Data.timeElapsed = (time)
    boat_Data.Distance = (piece_Distance)

    """
    GPS Section
    """
    ref_lat = boat_Data.Latitude
    ref_lon = boat_Data.Longitude

    meters_per_deg_lat = 111320  # Approx. meters per degree latitude
    meters_per_deg_lon = meters_per_deg_lat * math.cos(math.radians(ref_lat))  # Longitude varies by latitude

    # Iterate through the GPS data lines in the grid.

    file.stream.seek(0) 
    for i, row in enumerate(iterRows(file)):
        if i < layout["GPS_Start_Line"]:
            continue
        if i >= layout["GPS_End_Line"]:
            break

        raw_lat = float(row[11])
        raw_lon = float(row[12])

        # Convert to Lon, Lat degrees
        delta_lat = raw_lat / meters_per_deg_lat
        delta_lon = raw_lon / meters_per_deg_lon
        lat_new = ref_lat + delta_lat
        lon_new = ref_lon + delta_lon

        # Append converted GPS data to boat data object dictionary
        boat_Data.data['GPS'].append([lon_new,lat_new])

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

            Recov_25_Difference = Recov_25_Time-Stroke_25_Recov[count]
            Recov_50_Difference = Recov_50_Time-Stroke_50_Recov[count]
            Recov_75_Difference = Recov_75_Time-Stroke_75_Recov[count]
            Hang_Difference = Hang_Time-Stroke_Hang[count]
            Min_Difference = Min_Time-Stroke_Min[count]
            Catch_Difference = Catch_Time-Stroke_Catch[count]
            Effective_Drive_Difference = Effective_Drive_Time-Stroke_Effective_Drive[count]
            MaxF70_Difference = MaxF70_Time-Stroke_70Max_F[count]
            MaxF_Difference = MaxF_Time-Stroke_MaxF[count]
            MaxFrom70_Difference = MaxFrom70_Time-Stroke_From70Max_F[count]
            FSlip_Difference = FSlip_Time-Stroke_FSlip[count]
            Finish_Difference = Finish_Time-Stroke_Finish[count]
            Max_Difference = Max_Time-Stroke_Max[count]
            Recovery_Difference = Recovery_Time-Stroke_Recovery[count]

            # Add calculated differences to rower data object dictionary
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

    # Data is returned to setup_data.py line 106 as a list

    return profiles_List, boat_Data