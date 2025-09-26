# Main imports
from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_session import Session
import os
import requests

# API Routes
import API_Routes

# 
from Telemetry.setup_data import set_session_classes
from Telemetry.api_requests.get_summary import get_summary
from Telemetry.api_requests.get_averages import get_averages

# Dashboard
from Telemetry.graphs.dashboard.avg_syncronisation import get_avg_syncronisation_dashboard
from Telemetry.graphs.dashboard.avg_syncronisation import get

# Samples - Sessions
from Telemetry.graphs.sample_plot.sample_syncronisation_plots import get_sample_syncronisation_plots
from Telemetry.graphs.sample_plot.sample_ratio_plots import get_sample_ratio_plots
from Telemetry.graphs.sample_plot.sample_line import get_sample_line_plots

# Average - Sessions
from Telemetry.graphs.average_plot.avg_sync import get_avg_syncronisation_plot
from Telemetry.graphs.average_plot.avg_ratio import get_avg_ratio_plot
from Telemetry.graphs.average_plot.avg_line import get_avg_line_plot

# Retrieve data
from Telemetry.api_requests.get_sessions import get_sessions
from Telemetry.api_requests.get_rower_data import get_rower_data

# Setup flask settings
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'e9f8a7d9a8fbd0c44a3ff0e1b7351f3c7b1a64e8f9e3b0e59f46a8cbb3e72c9f'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Home Page
@app.route('/')
def home():
    # Automatically load all slideshow images
    slideshow_folder = os.path.join(app.static_folder, 'Media/Slideshow')
    images = [f'Media/Slideshow/{img}' for img in os.listdir(slideshow_folder)]
    return render_template(
        'index.html', 
        images=images
    )

# Showcase Page
@app.route('/showcase')
def showcase():
    return render_template(
        'showcase.html'
    )

# Register User Page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template(
                "register.html", 
                error='Passwords do not match. Please try again.'
            )

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }

        response = requests.post(API_Routes.create_user, json=payload)

        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            return render_template(
                "register.html", 
                error="Email is already in use for another account."
            )

    return render_template('register.html')

# Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        payload = {
            "email": email,
            "password": password
        }

        response = requests.get(API_Routes.check_user, json=payload)
        if response.status_code == 200:
            user_data = response.json()
            session['user'] = user_data
            return redirect(url_for('dashboard'))
        
        elif response.status_code == 401:
            return render_template(
                "login.html", 
                error="Username or Password incorrect."
            )

    return render_template('login.html')

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    # Login check
    if "user" not in session:
        return redirect(url_for('login'))
    
    user_summary = get_summary(session['user']['id'])
    data_averages = get_averages(session['user']['id'])
    print(data_averages)

    returned_graphs = {
        'radar': get_avg_syncronisation_dashboard(session['user']['id']),
        'gateforcex': get_avg_gateforcex_dashboard(session['user']['id'])
    }

    return render_template(
        "dashboard.html", 
        page='dashboard', 
        user=session['user'], 
        summary=user_summary, 
        averages=data_averages, 
        graphs=returned_graphs
    )

@app.route('/dashboard/upload', methods=['GET', 'POST'])
def upload():
    # Login check
    if "user" not in session:
        return redirect(url_for('login'))
    
    if not session['user']['is_coach']:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        button_pressed = request.form.get('action')
        if button_pressed == 'upload':
            file = request.files['file']
            if file:
                session_classes = set_session_classes(file)

                Rower_Profiles = session_classes[0]
                Boat_Data = session_classes[1]

                # So I can access rower_profiles without having to re calculate all the data.
                session['rower_profiles'] = [rower.to_dict() for rower in Rower_Profiles]
                session['boat_data'] = Boat_Data.to_dict()

                return render_template(
                    "dashboard.html",
                    page="upload",
                    rowers=Rower_Profiles,
                    user=session['user'], 
                    show_upload_modal=True
                )
    
        elif button_pressed == 'confirm_upload':
            # Retrieve session storage from file upload.
            Rower_Profiles = session.get("rower_profiles")
            Boat_Data = session.get("boat_data")

            # Save boat_data to database and store the primary key in the return
            print(request.form.get('description_input'))
            Boat_Data['coach_id'] = session.get('user')['id']
            Boat_Data['description'] = request.form.get('description_input')
            Boat_Data['state'] = request.form.get('state_selected')

            # API post
            response = requests.post(API_Routes.upload_session, json=Boat_Data)
            session_id = response.json()['session_id']

            # Iterate through the rower profiles saved then save to database.
            for rower in Rower_Profiles:
                seat = str(rower["seat"])
                user_id = request.form.get(f"user_search_{seat}")
                # Upload user data to DB
                if user_id:
                    rower['user_id'] = int(user_id)
                else:
                    rower['user_id'] = None

                rower['session_id'] = int(session_id)
                response = requests.post(API_Routes.upload_user_data, json=rower)

            redirect(url_for('sessions'))
            
    return render_template(
        "dashboard.html", 
        page="upload", 
        user=session['user']
    )

@app.route('/dashboard/sessions', methods=['GET', 'POST'])
def sessions():
    if "user" not in session:
        return redirect(url_for('login'))
    
    returned_sessions = get_sessions(session['user']['id'])
    session['all_sessions'] = returned_sessions

    return render_template(
        "dashboard.html", 
        page="sessions", 
        sessions=session['all_sessions'],
        user=session['user']
    )

@app.route('/dashboard/sessions/<int:session_id>/<page_name>', methods=['GET', 'POST'])
def session_page(session_id, page_name):
    # Is user logged in
    if "user" not in session:
        return redirect(url_for('login'))
    
    # Get session from cache
    session_data = None
    for rowing_session in session['all_sessions']:
        if rowing_session['id'] == session_id:
            session_data = rowing_session
            break

    # If not session found
    if not session_data:
        return redirect(url_for('sessions'))
    
    # Handle session deletion
    if request.method == 'POST' and request.form.get('action') == 'delete_session':
        # Check if user is a coach
        if not session['user'].get('is_coach', False):
            flash('You are not authorized to delete sessions.', 'error')
            return redirect(url_for('sessions', session_id=session_id, page_name=page_name))

        try:
            # Make API call to delete session
            response = requests.delete(f"{API_Routes.delete_session}/{session_id}")
            if response.status_code == 200:
                # Update session cache by removing the deleted session
                session['all_sessions'] = [s for s in session['all_sessions'] if s['id'] != session_id]
                flash('Session deleted successfully.', 'success')
                return redirect(url_for('sessions'))
            else:
                flash(f'Failed to delete session. Status code: {response.status_code}', 'error')
        except requests.RequestException as e:
            flash(f'Error deleting session: {str(e)}', 'error')
        return redirect(url_for('sessions', session_id=session_id, page_name=page_name))
    
    # Checks if user is valid in session
    if not session['user']['is_coach']:
        is_Authenticated = False
        for rower in rowing_data:
            if rower.user_id == session['user']['id']:
                is_Authenticated = True

        if not is_Authenticated:
            redirect(url_for('sessions'))

    # Get Rower Data
    rowing_data = get_rower_data(session_id)

    # Generate graphs
    if page_name == 'samples':
        returned_graphs = {
            "syncronisation": get_sample_syncronisation_plots(rowing_data),
            "ratios": get_sample_ratio_plots(rowing_data),
            "gateforcex": get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'gate_force_x', 'GateForceX', '% Of Cycle', 'Gate Force X (kg)'),
            "gateanglevelocity": get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'gate_angle_vel', 'GateAngle Velocity', '% Of Cycle', 'Gate Angle Vel (deg/s)'),
            "legsvelocity": get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'seat_posn_vel', 'Legs Velocity','% Of Cycle', 'Legs Vel (deg)'),
            "seatposition": get_sample_line_plots(rowing_data, 'gate_angle', 'seat_posn', 'Seat Position', 'Gate Angle (deg)', 'Seat Position'),
            "legsvelocitygateangle": get_sample_line_plots(rowing_data, 'percent_of_arc', 'seat_posn_vel', 'Legs Velocity', 'Drive Length %', 'Legs Velocity (mm/s)'),
            "bodyarmsvelocity": get_sample_line_plots(rowing_data, 'percent_of_arc', 'body_arms_vel', 'Body + Arms Velocity', 'Drive Length %', 'Body Arms Vel (deg/s)')
        }
    elif page_name == 'average':
        returned_graphs = {
            "syncronisation": get_avg_syncronisation_plot(rowing_data),
            "ratios": get_avg_ratio_plot(rowing_data),
            "gateforcex": get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'gate_force_x', 'GateForceX', '% Of Cycle', 'Gate Force X (kg)'),
            "gateanglevelocity": get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'gate_angle_vel', 'GateAngle Velocity', '% Of Cycle', 'Gate Angle Vel (deg)'),
            "legsvelocity": get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'seat_posn_vel', 'Legs Velocity','% Of Cycle', 'Legs Vel (deg)'),
            "seatposition": get_avg_line_plot(rowing_data, 'gate_angle', 'seat_posn', 'Seat Position', 'Gate Angle (deg)', 'Seat Position'),
            "legsvelocitygateangle": get_avg_line_plot(rowing_data, 'percent_of_arc', 'seat_posn_vel', 'Legs Velocity', 'Drive Length %', 'Legs Velocity (mm/s)'),
            "bodyarmsvelocity": get_avg_line_plot(rowing_data, 'percent_of_arc', 'body_arms_vel', 'Body + Arms Velocity', 'Drive Length %', 'Body Arms Vel (deg/s)')
        }
    else:
        returned_graphs = {}

    # Render the page with the correct data
    return render_template(
        "dashboard.html",
        page=page_name,
        rowers=rowing_data,
        boat_data=session_data,
        user=session['user'],
        graphs=returned_graphs
    )


@app.route('/dashboard/admin', methods=['GET', 'POST'])
def admin():
    if "user" not in session:
        return redirect(url_for('login'))
    
    if not session['user']['is_admin']:
        return redirect(url_for('dashboard'))

    response = requests.get(API_Routes.get_all_users)
    if response.status_code == 200:
        all_users = response.json()
    else:
        all_users = []

    return render_template(
        "dashboard.html", 
        page="admin", 
        all_users=all_users,
        user=session['user']
    )

@app.route('/dashboard/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    response = requests.delete(f"{API_Routes.delete_user}/{user_id}")
    if response.status_code == 200:
        flash('Session deleted successfully.', 'success')
    else:
        flash(f'Failed to delete session. Status code: {response.status_code}', 'error')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)