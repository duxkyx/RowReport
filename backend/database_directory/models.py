from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import date

# User Table
class account_table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, unique=True, nullable=False)
    password: str

# Permissions Table
class permissions_table(SQLModel, table=True):
    user_id: int = Field(foreign_key='account_table.id', primary_key=True)
    is_admin: bool = Field(default=False)
    is_coach: bool = Field(default=False)
    is_athlete: bool = Field(default=True)

# Boat Data Table (one (self) to many (user_telemetry_data))
class rowing_session_table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    coach_id: Optional[int] = Field(foreign_key='account_table.id') # Coach who uploaded the data
    
    title: str
    description: Optional[str]
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

    rating: List[float] = Field(sa_column=Column(JSON))
    averagepower: List[float] = Field(sa_column=Column(JSON))
    distanceperstroke: List[float] = Field(sa_column=Column(JSON))
    stroketime: List[float] = Field(sa_column=Column(JSON))
    meterspersecond: List[float] = Field(sa_column=Column(JSON))
    normalizedcatch: List[float] = Field(sa_column=Column(JSON))
    normalizedfinish: List[float] = Field(sa_column=Column(JSON))
    sample_time: List[float] = Field(sa_column=Column(JSON))
    sample_strokes: List[int] = Field(sa_column=Column(JSON))
    
    # 2D arrays
    acceleration: List[List[float]] = Field(sa_column=Column(JSON))
    normalizedtime: List[List[float]] = Field(sa_column=Column(JSON))

    boatroll: List[List[float]] = Field(sa_column=Column(JSON))
    boatpitch: List[List[float]] = Field(sa_column=Column(JSON))
    boatyaw: List[List[float]] = Field(sa_column=Column(JSON))

    # GPS 3D array
    gps: List[List[List[float]]] = Field(sa_column=Column(JSON))


# Rower Profiles Table
class user_telemetry_data(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: Optional[int] = Field(foreign_key='account_table.id', nullable=True) # Athlete who the data belongs to
    session_id: int = Field(foreign_key='rowing_session_table.id') # Session the data belongs to

    seat: int
    side: str
    name: str
    strokes: int

    min_angle: List[float] = Field(sa_column=Column(JSON))
    max_angle: List[float] = Field(sa_column=Column(JSON))
    arc_length: List[float] = Field(sa_column=Column(JSON))
    catch_slip: List[float] = Field(sa_column=Column(JSON))
    finish_slip: List[float] = Field(sa_column=Column(JSON))
    rower_swivel_power: List[float] = Field(sa_column=Column(JSON))
    seat_length: List[float] = Field(sa_column=Column(JSON))
    catch_factor: List[float] = Field(sa_column=Column(JSON))

    max_gate_force_x: List[float] = Field(sa_column=Column(JSON))
    average_gate_force_x: List[float] = Field(sa_column=Column(JSON))
    position_of_maxf: List[float] = Field(sa_column=Column(JSON))
    catch_force_gradient: List[float] = Field(sa_column=Column(JSON))
    finish_force_gradient: List[float] = Field(sa_column=Column(JSON))
    legs_max_vel: List[float] = Field(sa_column=Column(JSON))

    power_timeline: List[float] = Field(sa_column=Column(JSON))

    # 2D arrays
    gate_force_x: List[List[float]] = Field(sa_column=Column(JSON))
    gate_angle: List[List[float]] = Field(sa_column=Column(JSON))
    gate_angle_vel: List[List[float]] = Field(sa_column=Column(JSON))
    seat_posn: List[List[float]] = Field(sa_column=Column(JSON))
    seat_posn_vel: List[List[float]] = Field(sa_column=Column(JSON))
    body_arms_vel: list[list[float]] = Field(sa_column=Column(JSON))

    # Bar Plot
    recovery_time_1: List[float] = Field(sa_column=Column(JSON))
    recovery_time_2: List[float] = Field(sa_column=Column(JSON))
    recovery_time_3: List[float] = Field(sa_column=Column(JSON))
    recovery_time_4: List[float] = Field(sa_column=Column(JSON))
    hang_time_1: List[float] = Field(sa_column=Column(JSON))
    hang_time_2: List[float] = Field(sa_column=Column(JSON))
    catch_slip_time: List[float] = Field(sa_column=Column(JSON))
    drive_time_1: List[float] = Field(sa_column=Column(JSON))
    drive_time_2: List[float] = Field(sa_column=Column(JSON))
    drive_time_3: List[float] = Field(sa_column=Column(JSON))
    drive_time_4: List[float] = Field(sa_column=Column(JSON))
    finish_slip_time: List[float] = Field(sa_column=Column(JSON))
    pause_time_1: List[float] = Field(sa_column=Column(JSON))
    pause_time_2: List[float] = Field(sa_column=Column(JSON))
    recovery_time_5: List[float] = Field(sa_column=Column(JSON))

    stroke_time: List[float] = Field(sa_column=Column(JSON))
    drive_time: List[float] = Field(sa_column=Column(JSON))
    recovery_time: List[float] = Field(sa_column=Column(JSON))

    # Synchronisation
    difference_25: List[float] = Field(sa_column=Column(JSON))
    difference_50: List[float] = Field(sa_column=Column(JSON))
    difference_75: List[float] = Field(sa_column=Column(JSON))
    difference_hang: List[float] = Field(sa_column=Column(JSON))
    difference_min: List[float] = Field(sa_column=Column(JSON))
    difference_catch: List[float] = Field(sa_column=Column(JSON))
    difference_effective_start: List[float] = Field(sa_column=Column(JSON))
    difference_70max: List[float] = Field(sa_column=Column(JSON))
    difference_maxf: List[float] = Field(sa_column=Column(JSON))
    difference_max70: List[float] = Field(sa_column=Column(JSON))
    difference_effective_end: List[float] = Field(sa_column=Column(JSON))
    difference_finish: List[float] = Field(sa_column=Column(JSON))
    difference_max: List[float] = Field(sa_column=Column(JSON))
    difference_recovery: List[float] = Field(sa_column=Column(JSON))

