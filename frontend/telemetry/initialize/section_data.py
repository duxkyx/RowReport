from telemetry.modules.sorting import section_Data, section_List, average_Array_into_Sections
from telemetry.initialize.data_map import mapping_athlete, mapping_session

# For individual rower data
def section_rower_data(rower_dict, boat_Data, new_Class):
    TWO_D_KEYS = {"GateForceX", "GateAngle", "GateAngleVel", "SeatPosn", "SeatPosnVel", "BodyArmsVel"}
    for src_key, dest_attr in mapping_athlete.items():
        values = rower_dict.get(src_key, [])
        if not None in values:
            if src_key in TWO_D_KEYS:
                sectioned = section_List(values, boat_Data)
                setattr(new_Class, dest_attr, average_Array_into_Sections(sectioned))
            elif src_key == 'Rower Swivel Power':
                setattr(new_Class, 'power_timeline', values)
                setattr(new_Class, dest_attr, section_Data(values, boat_Data))
            else:
                setattr(new_Class, dest_attr, section_Data(values, boat_Data))
        else:
            setattr(new_Class, dest_attr, [])
                
    return new_Class

# For session boat data
def section_boat_data(boat_dict, boat_Data, new_Class):
    TWO_D_KEYS = {"Acceleration", "Normalized Time"}
    for src_key, dest_attr in mapping_session.items():
        values = boat_dict.get(src_key, [])
        if src_key in TWO_D_KEYS:
            sectioned = section_List(values, boat_Data)
            setattr(new_Class, dest_attr, average_Array_into_Sections(sectioned))
        elif src_key == "GPS":
            sectioned = section_List(values, boat_Data)
            setattr(new_Class, dest_attr, sectioned)
        else:
            setattr(new_Class, dest_attr, section_Data(values, boat_Data))

    return new_Class