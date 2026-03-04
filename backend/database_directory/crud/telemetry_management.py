from sqlmodel import Session, select, or_
from database_directory.models import account_table, rowing_session_table, user_telemetry_data, permissions_table, coxswain_in_session_table
from database_directory.crud.user_management import get_account_information

# Add session to database
def add_session(session: Session, data):
    db_obj = rowing_session_table(**data.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return {"session_id": db_obj.id}

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
    if results.is_coach:
        user_type = 'Coach'
    if results.is_admin:
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

    session_result = None

    global_Select = (
        select(
            rowing_session_table.id,
            rowing_session_table.title,
            rowing_session_table.state,
            rowing_session_table.date,
            rowing_session_table.seats,
            rowing_session_table.tstrokes,
            rowing_session_table.distance,
            rowing_session_table.timeelapsed,
            rowing_session_table.coach_id
        )
        .select_from(rowing_session_table)
        .order_by(rowing_session_table.id.desc())
    )

    if permissions.is_admin or permissions.is_coach:
        session_statement = (global_Select)
        session_result = session.exec(session_statement).mappings().all()
    else:
        # normal users should see any sessions they have telemetry data for
        # *and* any sessions where they were recorded as the coxswain
        session_statement = (
            global_Select
            # join telemetry data so that users who rowed are included
            .join(user_telemetry_data, rowing_session_table.id == user_telemetry_data.session_id, isouter=True)
            # also outer‑join the coxswain table so we can filter by coxswain id
            .join(coxswain_in_session_table, rowing_session_table.id == coxswain_in_session_table.session_id, isouter=True)
            .where(
                or_(
                    user_telemetry_data.user_id == user_id,
                    coxswain_in_session_table.coxswain_id == user_id
                )
            )
            .distinct(rowing_session_table.id)
        )
        session_result = session.exec(session_statement).mappings().all()
    
    return session_result

# Returns the details for a given session
def get_session_details(session: Session, session_id: int):
    session_statement = (
        select(rowing_session_table)
        .where(rowing_session_table.id == session_id)
    )
    session_result = session.exec(session_statement).first()
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

def add_coxswain_data(session: Session, data):
    db_obj = coxswain_in_session_table(**data.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_coxswain_in_session(session: Session, session_id: int):
    statement = (
        select(coxswain_in_session_table, account_table)
        .join(account_table, coxswain_in_session_table.coxswain_id == account_table.id)
        .where(coxswain_in_session_table.session_id == session_id)
    )
    result = session.exec(statement).first()
    if result:
        coxswain_info = {
            "user_id": result.account_table.id,
            "first_name": result.account_table.first_name,
            "last_name": result.account_table.last_name,
            "email": result.account_table.email
        }
        return coxswain_info
    else:
        return None


def update_rower_assignment(session: Session, session_id: int, seat: int, user_id: int | None):
    """
    Update the `user_id` for a specific seat in a session's user_telemetry_data record.
    If user_id is None the assignment is cleared.
    Returns the updated row or None if not found.
    """
    statement = (
        select(user_telemetry_data)
        .where(user_telemetry_data.session_id == session_id)
        .where(user_telemetry_data.seat == seat)
    )
    db_obj = session.exec(statement).first()
    if not db_obj:
        return None

    db_obj.user_id = user_id
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_coxswain(session: Session, session_id: int, coxswain_id: int | None):
    """
    Set or clear the coxswain for a session.
    Creates a record if none exists.
    """
    statement = (
        select(coxswain_in_session_table)
        .where(coxswain_in_session_table.session_id == session_id)
    )
    db_obj = session.exec(statement).first()
    if db_obj:
        db_obj.coxswain_id = coxswain_id
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    else:
        new_obj = coxswain_in_session_table(session_id=session_id, coxswain_id=coxswain_id)
        session.add(new_obj)
        session.commit()
        session.refresh(new_obj)
        return new_obj


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