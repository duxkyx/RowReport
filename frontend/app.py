# Main imports
from flask import Flask, render_template, url_for, request, session, flash, redirect, send_file
from flask_session import Session
from functools import wraps
import requests
import io

# API Routes
import api_routes

# 
from telemetry.initialize.setup_data import set_session_classes
from telemetry.api_requests.get_summary import get_summary
from telemetry.api_requests.get_averages import get_averages

"""
Graph Imports
To keep code clean and modular, each graph type is imported from its own module.
For different types of graphs (linear, bar, radar, etc.), there are separate modules.
This allows for easier maintenance and scalability of the codebase.
"""
# Dashboard
from telemetry.graphs.specific.dashboard.avg_syncronisation import get_avg_syncronisation_dashboard
from telemetry.graphs.specific.dashboard.avg_gateforcex import get_avg_gateforcex_dashboard

# Graph creation
from telemetry.graphs.generate_graphs import return_Graphs

# Retrieve data
from telemetry.api_requests.get_sessions import get_sessions
from telemetry.api_requests.get_rower_data import get_rower_data

# PDF Report
from telemetry.export.pdf import generate_pdf

# Setup flask settings
app = Flask(__name__, template_folder='templates', static_folder='static')

# Secret key for sessions
app.secret_key = 'e9f8a7d9a8fbd0c44a3ff0e1b7351f3c7b1a64e8f9e3b0e59f46a8cbb3e72c9f'

# Configure session to use filesystem (to store large objects temporarily such as uploaded files)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "large_session_cache"  # folder for temp objects
app.config["SESSION_PERMANENT"] = False  # optional

# Initialize the filesystem session
Session(app)

# Define login required decorator
def login_required(origin):
    @wraps(origin)
    def decorated_function(*args, **kwargs): # Positional arguments and key word arguments, returns the data passed.
        if 'user' in session:
            return origin(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

# Define role-based access
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get('user')
            if (not user or user.get(role) != True) and (user.get('is_admin') != True):
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Home Page
@app.route('/')
def home():
    response = requests.get(api_routes.get_statistics)
    stats = {}
    if response.status_code == 200:
        stats = response.json()
    else:
        stats = {
            'users': 0,
            'uploads': 0,
            'strokes': 0,
            'distance': 0,
            'wattage': 0
        }   

    return render_template(
        'index.html', 
        statistics=stats
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
            "email": email.lower(),
            "password": password,
        }

        response = requests.post(api_routes.create_user, json=payload)

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
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        payload = {
            "email": email.lower(),
            "password": password
        }

        response = requests.get(api_routes.check_user, json=payload)
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

# Dashboard Page
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    user_summary = get_summary(session['user']['id'])
    data_averages = get_averages(session['user']['id'])

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

# Flask setup and render upload page
@app.route('/dashboard/upload', methods=['GET', 'POST'])
@login_required
@role_required('is_coach')
def upload():
    if request.method == 'POST':
        button_pressed = request.form.get('action')

        if button_pressed == 'upload':
            file = request.files['file']
            if file:
                try:
                    session_classes = set_session_classes(file)
                except Exception as e:
                    return render_template(
                        "dashboard.html", 
                        page="upload", 
                        user=session['user'],
                        error=f'Error processing file: {str(e)}: File possibly corrupted or invalid format.'
                    )
                
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
                    show_upload_modal=True,
                    apiroute_getallusers=api_routes.get_all_users
                )
    
        elif button_pressed == 'confirm_upload':
            # Retrieve session storage from file upload.
            Rower_Profiles = session.get("rower_profiles")
            Boat_Data = session.get("boat_data")

            # Save boat_data to database and store the primary key in the return
            Boat_Data['coach_id'] = session.get('user')['id'] # The user who uploaded the file
            Boat_Data['description'] = request.form.get('description_input')
            Boat_Data['state'] = request.form.get('state_selected')
            Boat_Data['title'] = request.form.get('title_input')

            # API post
            response = requests.post(api_routes.upload_session, json=Boat_Data)
            session_id = response.json()['session_id']

            if not response.status_code == 200:
                return render_template(
                    "dashboard.html", 
                    page="upload", 
                    user=session['user'],
                    error=f'Error saving data to database.'
                )

            # Iterate through the rower profiles then upload to database.
            for rower in Rower_Profiles:
                seat = str(rower["seat"])
                user_id = request.form.get(f"user_search_{seat}")

                # Upload user data to DB
                if user_id:
                    rower['user_id'] = int(user_id)
                else:
                    rower['user_id'] = None

                rower['session_id'] = int(session_id)
                response = requests.post(api_routes.upload_user_data, json=rower)

                if response.status_code == 200:
                    if user_id:
                        payload = {
                            "user_id": rower['user_id'],
                            "boat_data": Boat_Data,
                            "session_id": session_id
                        }
                        requests.post(api_routes.email_user, json=payload)
            
            # Email coach that upload was successful
            payload = {
                "user_id": Boat_Data['coach_id'],
                "boat_data": Boat_Data,
                "session_id": session_id
            }
            requests.post(api_routes.email_user, json=payload)

            return redirect(url_for('sessions'))
        
    return render_template(
        "dashboard.html", 
        page="upload", 
        user=session['user'],
    )

# Flask setup and render session selection page
@app.route('/dashboard/sessions', methods=['GET', 'POST'])
@login_required
def sessions():
    all_sessions = get_sessions(session['user']['id'])
    for rowing_session in all_sessions:
        coach_id = rowing_session['coach_id']

        # Check if coach exists in session
        if coach_id is None:
            rowing_session['coach_name'] = None
            continue

        # 
        get_coach_account_information = requests.post(f'{api_routes.get_user_information}/{coach_id}').json()
        coach_name = f'{get_coach_account_information['first_name']} {get_coach_account_information['last_name']}'
        rowing_session['coach_name'] = coach_name

    return render_template(
        "dashboard.html", 
        page="sessions", 
        sessions=all_sessions,
        user=session['user'],
    )

# Session analytics page
@app.route('/dashboard/sessions/session_id=<int:session_id>/page=<page_name>', methods=['GET', 'POST'])
@login_required
def session_page(session_id, page_name):
    # Get session data from API
    session_data = requests.get(api_routes.get_session + f'/{session_id}').json()

    # If not session found
    if not session_data:
        return redirect(url_for('sessions'))
        
    # Handle session deletion
    if request.method == 'POST' and request.form.get('action') == 'delete_session':
        # Check if user is a coach
        if not session['user'].get('is_coach', False) and not session['user'].get('is_admin', False):
            flash('You are not authorized to delete sessions.', 'error')
            return redirect(url_for('sessions', session_id=session_id, page_name=page_name))

        try:
            # Make API call to delete session
            response = requests.delete(f"{api_routes.delete_session}/{session_id}")
            if response.status_code == 200:
                return redirect(url_for('sessions'))
            else:
                flash(f'Failed to delete session. Status code: {response.status_code}', 'error')
        except requests.RequestException as e:
            flash(f'Error deleting session: {str(e)}', 'error')
        return redirect(url_for('sessions', session_id=session_id, page_name=page_name))
    
    # Get Rower Data
    rowing_data = get_rower_data(session_id)

    # Checks if user is valid in session
    if not session['user']['is_coach'] and not session['user']['is_admin']:
        is_Authenticated = False
        for rower in rowing_data:
            if rower['telemetry']['user_id'] == session['user']['id']:
                is_Authenticated = True

        if not is_Authenticated:
            return redirect(url_for('sessions'))

    name_array = []
    for user_data in rowing_data:
        if user_data['user']['user_id']:
            name_array.append(user_data['user']['last_name'])
        else:
            name_array.append(user_data['telemetry']['name'])

    # Generate graphs
    if page_name == 'samples' and request.method == 'POST':
        selected_sample = int(request.form.get('sample_id'))
    else:
        selected_sample = None

    returned_graphs = return_Graphs(
        page_name, 
        session_data,
        rowing_data,
        name_array,
        request,
        selected_sample
    )

    if request.method == 'POST':
        if page_name == 'export' and request.form.get('action') == 'download':
            pdf_bytes = generate_pdf(session_data, rowing_data, name_array, request)

            # Wrap in BytesIO for send_file
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_file.seek(0)

            flash(f'Downloading file. Please wait.', 'error')

            return send_file(
                pdf_file,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"session_{session_id}_report.pdf"
            )


    # Render the page with the correct data
    return render_template(
        "dashboard.html",
        page=page_name,
        rowers=rowing_data,
        boat_data=session_data,
        user=session['user'],
        graphs=returned_graphs,
        sample_selected=selected_sample
    )

# Admin page
@app.route('/dashboard/admin', methods=['GET', 'POST'])
@login_required
@role_required('is_admin')
def admin():
    response = requests.get(api_routes.get_all_users)
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

# Admin register user route
@app.route("/dashboard/admin/register_user", methods=["POST"])
def register_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    # Build payload for your API
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email.lower(),
        "password": password,
    }

    # Call your API
    response = requests.post(api_routes.create_user, json=payload)
    created_user = response.json()
    print(created_user)

    if response.status_code == 200:
        created_user = response.json()
        permission_response = requests.post(f'{api_routes.update_permissions}/{created_user["id"]}/{user_type}')
        if permission_response.status_code == 200:
            flash(f"User {first_name} {last_name} registered successfully!", "success")
        else:
            flash("User created but failed to update permissions.", "danger")
    else:
        try:
            error_msg = response.json().get("error", "Failed to register user.")
        except:
            error_msg = "Failed to register user."
        flash(error_msg, "danger")

    return redirect(url_for("admin"))

# Delete user route
@app.route('/dashboard/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('is_admin')
def delete_user(user_id):
    response = requests.delete(f"{api_routes.delete_user}/{user_id}")
    if response.status_code == 200:
        flash('User deleted successfully.', 'success')
    else:
        flash(f'Failed to delete user. Status code: {response.status_code}', 'error')
    return redirect(url_for('admin'))

# View account details page
@app.route('/dashboard/account')
@login_required
def account():
    return render_template(
        'dashboard.html',
        user=session['user'],
        page='account'
    )

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)