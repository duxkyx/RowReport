# Get the data required for the radar chart on the dashboard
import requests
import api_routes
from telemetry.modules.sorting import average_Array_into_One_Percentage as aaio

def get_gateforce_averages(user_id):
    response = requests.get(f"{api_routes.get_telemetry_data_training_zones}/{user_id}")
    if response.status_code == 200:
        training_zone_data = response.json()
        
        UT1_GateForce_Data = []
        UT1_xaxis = []
        UT2_GateForce_Data = []
        UT2_xaxis = []
        for telemetry in training_zone_data['UT1']:
            # telemetry['gate_force_x'] holds 8 arrays of large sizes
            # average them into one array and store
            UT1_GateForce_Data.append(aaio(telemetry['gate_force_x']))
            UT1_xaxis.append(aaio(telemetry['gate_angle']))

        for telemetry in training_zone_data['UT2']:
            UT2_GateForce_Data.append(aaio(telemetry['gate_force_x']))
            UT2_xaxis.append(aaio(telemetry['gate_angle']))

        if len(UT1_GateForce_Data) >= 1:
            ut1 = aaio(UT1_GateForce_Data)
            ut1_x = aaio(UT1_xaxis)
        else:
            ut1 = []
            ut1_x = []

        if len(UT2_GateForce_Data) >= 1:
            ut2 = aaio(UT2_GateForce_Data)
            ut2_x = aaio(UT2_xaxis)
        else:
            ut2 = []
            ut2_x = []

        return {
            "UT1": ut1,
            "UT2": ut2,
            "UT1_xaxis": ut1_x,
            "UT2_xaxis": ut2_x
        }

    else:
        return {
            "UT1": [],
            "UT2": [],
            "UT1_xaxis": [],
            "UT2_xaxis": []
        }