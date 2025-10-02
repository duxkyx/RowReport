from sqlmodel import Session, select, or_
from Database.models import account_table, rowing_session_table, user_telemetry_data, permissions_table

# Add session to database
def add_session(session: Session, data):
    db_obj = rowing_session_table(**data.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return {"session_id": db_obj.id}

# Delete session where session_id = given id
def delete_session(session: Session, session_id: int) -> rowing_session_table:
    statement = select(rowing_session_table).where(rowing_session_table.id == session_id)
    obj = session.exec(statement).first()
    if obj:
        session.delete(obj)
        session.commit()

    statement = select(user_telemetry_data).where(user_telemetry_data.session_id == session_id)
    obj = session.exec(statement).all()
    for record in obj:
        session.delete(record)
        session.commit()

    return obj

# Adds rower data to database
def add_rower_data(session: Session, data) -> user_telemetry_data:
    db_obj = user_telemetry_data(**data.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

# Gets the summary data for a user - Dashboard
def get_user_summary(session: Session, user_id: int):
    statement = (
        select(rowing_session_table)
        .join(user_telemetry_data, rowing_session_table.id == user_telemetry_data.session_id)
        .where(user_telemetry_data.user_id == user_id)
    )
    sessions = session.exec(statement).all()
    num_sessions = len(sessions)

    # Get total strokes and distance
    total_strokes = 0
    total_distance = 0.0
    for s in sessions:
        total_strokes += s.tstrokes
        total_distance += s.distance

    # Get user type
    permissions_statement = (
        select(permissions_table)
        .where(permissions_table.user_id == user_id)
    )
    results = session.exec(permissions_statement).first()
    
    user_type = 'N/A'
    if results.is_athlete:
        user_type = 'Athlete'
    elif results.is_coach:
        user_type = 'Coach'
    else:
        user_type = 'Administrator'

    return {
        "num_sessions": num_sessions,
        "total_strokes": total_strokes,
        "total_distance": total_distance,
        "user_type": user_type
    }

# Gets the average telemetry data for a user - Dashboard
def get_user_averages(session: Session, user_id: int):
    statement = (
        select(user_telemetry_data, rowing_session_table)
        .join(rowing_session_table, user_telemetry_data.session_id == rowing_session_table.id)
        .where(user_telemetry_data.user_id == user_id)
    )
    sessions = session.exec(statement).all()

    # Separate sessions by state
    ut1_sessions = []
    ut2_sessions = []

    for telemetry, session_data in sessions:
        if session_data.state == "UT1":
            ut1_sessions.append(telemetry)
        elif session_data.state == "UT2":
            ut2_sessions.append(telemetry)

    def safe_avg(values):
        return sum(values) / len(values) if values else 0

    def compute_averages(session_list):
        if not session_list:
            # Return zeroed summary if no data
            return {
                "min_angle": 0,
                "max_angle": 0,
                "arc_length": 0,
                "catch_slip": 0,
                "finish_slip": 0,
                "swivel_power": 0,
                "seat_length": 0
            }
        
        number_of_sessions = len(session_list)
        summary = {
            "min_angle": safe_avg([safe_avg(r.min_angle) for r in session_list if r.min_angle]),
            "max_angle": safe_avg([safe_avg(r.max_angle) for r in session_list if r.max_angle]),
            "arc_length": safe_avg([safe_avg(r.arc_length) for r in session_list if r.arc_length]),
            "catch_slip": safe_avg([safe_avg(r.catch_slip) for r in session_list if r.catch_slip]),
            "finish_slip": safe_avg([safe_avg(r.finish_slip) for r in session_list if r.finish_slip]),
            "swivel_power": safe_avg([safe_avg(r.rower_swivel_power) for r in session_list if r.rower_swivel_power]),
            "seat_length": safe_avg([safe_avg(r.seat_length) for r in session_list if r.seat_length]),
        }
        return summary

    return {
        'UT1': compute_averages(ut1_sessions),
        'UT2': compute_averages(ut2_sessions)
    }
    
# Gets the radar average telemetry data for a user - Dashboard
def get_user_radar_averages(session: Session, user_id: int):
    statement = (
        select(user_telemetry_data, rowing_session_table)
        .join(rowing_session_table, user_telemetry_data.session_id == rowing_session_table.id)
        .where(user_telemetry_data.user_id == user_id)
    )
    sessions = session.exec(statement).all()

    # Separate sessions by state
    ut1_sessions = []
    ut2_sessions = []

    for telemetry, session_data in sessions:
        if session_data.state == "UT1":
            ut1_sessions.append(telemetry)
        elif session_data.state == "UT2":
            ut2_sessions.append(telemetry)

    def compute_averages(session_list):
        if not session_list:
            return {key: 0 for key in [
                "25_recov", "50_recov", "75_recov", "hang_start", "min_angle",
                "catch", "effect_start", "70_max", "max_f", "max_70",
                "effect_end", "finish", "max_angle", "release"
            ]}
        
        count = len(session_list)
        return {
            "25_recov": sum(sum(s.difference_25)/len(s.difference_25) for s in session_list) / count,
            "50_recov": sum(sum(s.difference_50)/len(s.difference_50) for s in session_list) / count,
            "75_recov": sum(sum(s.difference_75)/len(s.difference_75) for s in session_list) / count,
            "hang_start": sum(sum(s.difference_hang)/len(s.difference_hang) for s in session_list) / count,
            "min_angle": sum(sum(s.difference_min)/len(s.difference_min) for s in session_list) / count,
            "catch": sum(sum(s.difference_catch)/len(s.difference_catch) for s in session_list) / count,
            "effect_start": sum(sum(s.difference_effective_start)/len(s.difference_effective_start) for s in session_list) / count,
            "70_max": sum(sum(s.difference_70max)/len(s.difference_70max) for s in session_list) / count,
            "max_f": sum(sum(s.difference_maxf)/len(s.difference_maxf) for s in session_list) / count,
            "max_70": sum(sum(s.difference_max70)/len(s.difference_max70) for s in session_list) / count,
            "effect_end": sum(sum(s.difference_effective_end)/len(s.difference_effective_end) for s in session_list) / count,
            "finish": sum(sum(s.difference_finish)/len(s.difference_finish) for s in session_list) / count,
            "release": sum(sum(s.difference_max)/len(s.difference_max) for s in session_list) / count,
            "max_angle": sum(sum(s.difference_recovery)/len(s.difference_recovery) for s in session_list) / count
        }

    return {
        "UT1": compute_averages(ut1_sessions),
        "UT2": compute_averages(ut2_sessions)
    }

def get_user_telemetry_data(session: Session, user_id: int):
    statement = (
        select(user_telemetry_data, rowing_session_table)
        .join(rowing_session_table, user_telemetry_data.session_id == rowing_session_table.id)
        .where(user_telemetry_data.user_id == user_id)
    )
    sessions = session.exec(statement).all()

    # Separate sessions by training zone
    ut1_sessions = []
    ut2_sessions = []

    for telemetry, session_data in sessions:
        if session_data.state == "UT1":
            ut1_sessions.append(telemetry)
        elif session_data.state == "UT2":
            ut2_sessions.append(telemetry)

    return {
        "UT1": ut1_sessions,
        "UT2": ut2_sessions
    }

# Gets all sessions for a user - Sessions Page
def get_user_sessions(session: Session, user_id: int):
    get_permissions_statement = (
        select(permissions_table)
        .where(permissions_table.user_id == user_id)
    )
    permissions = session.exec(get_permissions_statement).first()

    if permissions.is_admin:
        session_statement = (
            select(rowing_session_table).order_by(rowing_session_table.id.desc())
        )
        session_result = session.exec(session_statement).all()
        return session_result
    if permissions.is_coach:
        session_statement = (
            select(rowing_session_table).order_by(rowing_session_table.id.desc())
            .where(rowing_session_table.coach_id == user_id)
        )
        session_result = session.exec(session_statement).all()
        return session_result
    else:
        session_statement = (
            select(rowing_session_table).order_by(rowing_session_table.id.desc())
            .join(user_telemetry_data, rowing_session_table.id == user_telemetry_data.session_id)
            .where(user_telemetry_data.user_id == user_id)
        )
        session_result = session.exec(session_statement).all()
        return session_result

# Returns all the rower data for a given session
def get_rower_data(session: Session, session_id: int):
    # Get all telemetry records for the session
    telemetry_statement = (
        select(user_telemetry_data)
        .where(user_telemetry_data.session_id == session_id)
        .order_by(user_telemetry_data.id.asc())
    )
    telemetry_results = session.exec(telemetry_statement).all()
    rower_data = []
    for telemetry in telemetry_results:
        if telemetry.user_id is not None:
            account_statement = select(account_table).where(account_table.id == telemetry.user_id)
            account = session.exec(account_statement).first()
        else:
            account = None

        if account:
            user_info = {
                "user_id": account.id,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "email": account.email
            }
        else:
            user_info = {
                "user_id": None,
                "first_name": "",
                "last_name": "",
                "email": ""
            }

        rower_data.append({
            "telemetry": telemetry,
            "user": user_info
        })

    return rower_data

def delete_session(session: Session, session_id: int):
    # Deletes all user_telemetry_data records first, due to foriegn keys blocking the deletion of rowing_session_table
    user_statement = (
        select(user_telemetry_data)
        .where(user_telemetry_data.session_id == session_id)
    )
    statement_result = session.exec(user_statement).all()
    for record in statement_result:
        session.delete(record)
    session.commit()

    # Delete the session record
    session_statement = (
        select(rowing_session_table)
        .where(rowing_session_table.id == session_id)
    )

    statement_result = session.exec(session_statement).first()
    session.delete(statement_result)
    session.commit()
    return statement_result