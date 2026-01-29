from sqlmodel import Session, select, or_
from database_directory.models import account_table, rowing_session_table, user_telemetry_data, permissions_table

def get_statistics(session: Session):
    rowing_session_statement = (
        select(rowing_session_table)
    )
    sessions = session.exec(rowing_session_statement).all()

    user_statement = (
        select(account_table)
    )
    accounts = session.exec(user_statement).all()

    telemetry_statement = (
        select(user_telemetry_data)
    )
    
    telemetry = session.exec(telemetry_statement).all()
    
    return {
        'users': len(accounts),
        'uploads': len(sessions),
        'strokes': sum(r.tstrokes for r in sessions),
        'distance': sum(r.distance for r in sessions),
        'wattage': sum(sum(r.power_timeline) for r in telemetry)
    }