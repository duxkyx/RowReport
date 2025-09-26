# Gets user sessions for session page
import requests
import API_Routes

def get_sessions(user_id):
    response = requests.get(f"{API_Routes.get_sessions}/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    