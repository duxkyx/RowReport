from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Accounts
class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Telemetry Data
class BoatTelemetryData(BaseModel):
    coach_id: int

    title: str
    description: str
    state: str #UT1, UT2
    filename: str
    boatname: str
    category: str
    inboard: str
    oarlength: str
    seats: int
    tstrokes: int
    distance: float
    timeelapsed: str
    boattype: str
    date: str
    serial: str
    seat_sensors: bool

    rating: List[float]
    averagepower: List[float]
    distanceperstroke: List[float]
    stroketime: List[float]
    meterspersecond: List[float]
    normalizedcatch: List[float]
    normalizedfinish: List[float]
    sample_time: List[float] 
    sample_strokes: List[int]
    
    # 2D arrays
    acceleration: List[List[float]]
    normalizedtime: List[List[float]]
    boatroll: List[List[float]]
    boatpitch: List[List[float]]
    boatyaw: List[List[float]]

    # GPS 3D Array
    gps: List[List[List[float]]]


class UserTelemetryData(BaseModel):
    user_id: Optional[int] = None
    session_id: int
    
    seat: int
    side: str
    name: str
    strokes: int

    min_angle: List[float]
    max_angle: List[float]
    arc_length: List[float]
    catch_slip: List[float]
    finish_slip: List[float]
    rower_swivel_power: List[float]
    seat_length: List[float]
    catch_factor: List[float]

    max_gate_force_x: List[float]
    average_gate_force_x: List[float]
    position_of_maxf: List[float]
    catch_force_gradient: List[float] 
    finish_force_gradient: List[float]
    legs_max_vel: List[float]

    power_timeline: List[float]

    # 2D arrays
    gate_force_x: List[List[float]]
    gate_angle: List[List[float]]
    gate_angle_vel: List[List[float]]
    seat_posn: List[List[float]]
    seat_posn_vel: List[List[float]]
    body_arms_vel: list[list[float]]

    # Bar plot times
    recovery_time_1: List[float]
    recovery_time_2: List[float]
    recovery_time_3: List[float]
    recovery_time_4: List[float]
    hang_time_1: List[float]
    hang_time_2: List[float]
    catch_slip_time: List[float]
    drive_time_1: List[float]
    drive_time_2: List[float]
    drive_time_3: List[float]
    drive_time_4: List[float]
    finish_slip_time: List[float]
    pause_time_1: List[float]
    pause_time_2: List[float]
    recovery_time_5: List[float]

    stroke_time: List[float]
    drive_time: List[float]
    recovery_time: List[float]

    # Synchronisation
    difference_25: List[float]
    difference_50: List[float]
    difference_75: List[float]
    difference_hang: List[float]
    difference_min: List[float]
    difference_catch: List[float]
    difference_effective_start: List[float]
    difference_70max: List[float]
    difference_maxf: List[float]
    difference_max70: List[float]
    difference_effective_end: List[float]
    difference_finish: List[float]
    difference_max: List[float]
    difference_recovery: List[float]

