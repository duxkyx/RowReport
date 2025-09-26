# Gets user sessions for session page
import requests
import API_Routes

def get_rower_data(session_id):
    response = requests.get(f"{API_Routes.get_rower_data}/{session_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    