from sqlmodel import Session, select, or_
from database_directory.models import account_table, rowing_session_table, user_telemetry_data, permissions_table

# Add user to database
def create_user(session: Session, data):
    statement = select(account_table).where(account_table.email == data.email)
    if session.exec(statement).first():
        raise ValueError("Email already registered")

    user = account_table(first_name=data.first_name, last_name=data.last_name, email=data.email, password=data.password)
    session.add(user)
    session.commit()
    session.refresh(user)

    permission = permissions_table(user_id=user.id, is_admin=False, is_coach=False, is_athlete=True)
    session.add(permission)
    session.commit()
    session.refresh(permission)
    return user

# Login Check
def authenticate_user(session: Session, data):
    statement = (
        select(account_table, permissions_table)
        .join(permissions_table, account_table.id == permissions_table.user_id)
        .where(account_table.email == data.email)
    )
    result = session.exec(statement).first()
    
    if not result:
        return None
    
    user, permissions = result
    if user.password != data.password:
        return None
    
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_athlete": permissions.is_athlete,
        "is_coach": permissions.is_coach,
        "is_admin": permissions.is_admin
    }

# Returns all users
def get_all_users(session: Session, order: str = None):
    if order:
        statement = (
            select(account_table, permissions_table)
            .where(account_table.first_name.ilike(f"%{order}%") | account_table.last_name.ilike(f"%{order}%") | account_table.email.ilike(f"%{order}%"))
            .order_by(account_table.first_name.asc())
            .join(permissions_table, account_table.id == permissions_table.user_id)
        )
    else:
        statement = (
            select(account_table, permissions_table).order_by(account_table.id.asc())
            .join(permissions_table, account_table.id == permissions_table.user_id)
        )
    results = session.exec(statement).all()

    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_athlete": permissions.is_athlete,
            "is_coach": permissions.is_coach,
            "is_admin": permissions.is_admin
        }
        for user, permissions in results
    ]

def delete_user(session: Session, user_id: int):
    statement_records = (
        select(user_telemetry_data)
        .where(user_telemetry_data.user_id == user_id)
    )
    results = session.exec(statement_records).all()
    for row in results:
        row.user_id = None
    
    statement_permission_table = (
        select(permissions_table)
        .where(permissions_table.user_id == user_id)
    )
    statement_result = session.exec(statement_permission_table).first()
    session.delete(statement_result)

    statement_account_table = (
        select(account_table)
        .where(account_table.id == user_id)
    )
    statement_result = session.exec(statement_account_table).first()
    session.delete(statement_result)
    session.commit()

    return {"status": "success", "user_id": user_id}

def get_account_information(session: Session, user_id: int):
    statement = select(account_table).where(account_table.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise ValueError("User not found")
    return user