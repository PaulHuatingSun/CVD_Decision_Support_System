import streamlit as st
import psycopg2
from psycopg2 import Error
import pickle
import numpy as np

# Load the Gradient Boosting model using pickle
with open('gb_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Database connection setup
def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        psycopg2 connection object: Connection to the PostgreSQL database.
    """
    return psycopg2.connect(host='127.0.0.1', dbname='DSS', user='dadb')

def authenticate_user(username, password):
    """
    Authenticates the user based on the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        tuple: A tuple containing the user ID and user type if authentication is successful, otherwise (None, None).
    """
    user_id, user_type = None, None  # Initialize variables to None
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT \"User ID\", \"User Type\" FROM users WHERE \"username\" = %s AND \"password\" = %s", (username, password))
    user_info = cur.fetchone()
    cur.close()
    conn.close()
    if user_info:
        user_id, user_type = user_info
        user_type = user_type.strip().lower()
    return user_id, user_type

def convert_gender_to_number(gender):
    """
    Converts gender text to numerical representation.

    Args:
        gender (str): The gender text.

    Returns:
        int: Numerical representation of gender (1 for Male, 2 for Female).
    """
    return 1 if gender == "Male" else 2  # Default to 2 if not "Male"

def convert_number_to_gender(number):
    """
    Converts numerical representation of gender to text.

    Args:
        number (int): Numerical representation of gender (1 for Male, 2 for Female).

    Returns:
        str: Text representation of gender.
    """
    return "Male" if number == 1 else "Female"

# Define functions for converting between binary text and numerical representation
def convert_to_number(text):
    return 1 if text == "Yes" else 0

def convert_to_text(number):
    return "Yes" if number == 1 else "No"

def convert_level_to_number(level):
    """
    Converts text representation of a level to its numerical representation.

    Args:
        level (str): Text representation of the level.

    Returns:
        int: Numerical representation of the level.
    """
    level_map = {
        "Normal": 1,
        "Above Normal": 2,
        "Well Above Normal": 3
    }
    return level_map.get(level, 1)  # Default to 1 if not found

def convert_number_to_level(number):
    """
    Converts numerical representation of a level to its text representation.

    Args:
        number (int): Numerical representation of the level.

    Returns:
        str: Text representation of the level.
    """
    level_map = {
        1: "Normal",
        2: "Above Normal",
        3: "Well Above Normal"
    }
    return level_map.get(number, "Normal") 

# Definitions for the options in each select box
bp_options = ["Normal", "Above Normal", "Well Above Normal"]

def get_index_from_level(level, options):
    """
    Retrieves the index of a level in the given options list.

    Args:
        level (str): Text representation of the level.
        options (list): List of options.

    Returns:
        int: Index of the level in the options list.
    """
    try:
        return options.index(level)
    except ValueError:
        return 0

def analyze_blood_pressure(diastolic_bp, systolic_bp):
    """
    Analyzes blood pressure levels and provides feedback for the user.

    Args:
        diastolic_bp (float): Diastolic blood pressure value.
        systolic_bp (float): Systolic blood pressure value.
    """
    # Diastolic BP
    if diastolic_bp < 80:
        st.success("Your diastolic blood pressure is normal.")
    elif 80 <= diastolic_bp < 90:
        st.warning("Your diastolic blood pressure is at risk level. Consider monitoring it regularly. Recommended to adhere to a low-sodium diet and stay hydrated.")
    else:
        st.error("Your diastolic blood pressure is very high. Seek medical attention immediately.")

    # Systolic BP
    if systolic_bp < 120:
        st.success("Your systolic blood pressure is normal.")
    elif 120 <= systolic_bp < 140:
        st.warning("Your systolic blood pressure is at risk level. Consider monitoring it regularly. Recommend adhering to a low-sodium diet and staying hydrated.")
    else:
        st.error("Your systolic blood pressure is very high. Seek medical attention immediately.")

def analyze_cholesterol(cholesterol):
    """
    Analyzes cholesterol levels and provides feedback for the user.

    Args:
        cholesterol (str): Cholesterol level.
    """
    if cholesterol == "Normal":
        st.success("Your cholesterol level is normal.")
    elif cholesterol == "Above Normal":
        st.warning("Your cholesterol level is above normal. Recommended to have a diet low in saturated fats and cholesterol. Recommended to exercise 3 times a week.")
    else:
        st.error("Your cholesterol level is well above normal. Seek medical attention.")

def analyze_glucose(glucose):
    """
    Analyzes glucose levels and provides feedback for the user.

    Args:
        glucose (str): Glucose level.
    """
    if glucose == "Normal":
        st.success("Your glucose level is normal.")
    elif glucose == "Above Normal":
        st.warning("Your glucose level is above normal. Recommended to reduce intake of sugary and high-carbohydrate foods. Recommended to exercise 3 times a week.")
    else:
        st.error("Your glucose level is well above normal. Seek medical attention.")
        
# Helper Functions for analysis by physician
def analyze_blood_pressure_physician(diastolic_bp, systolic_bp):
    """
    Analyzes blood pressure levels and provides feedback for the physician.

    Args:
        diastolic_bp (float): Diastolic blood pressure value.
        systolic_bp (float): Systolic blood pressure value.
    """
    # Diastolic BP
    if diastolic_bp < 80:
        st.success("Patient's diastolic blood pressure is normal.")
    elif 80 <= diastolic_bp < 90:
        st.warning("Patient's diastolic blood pressure is at risk level. Consider monitoring it regularly. Recommend the patient to adhere to a low-sodium diet and stay hydrated.")
    else:
        st.error("Patient's diastolic blood pressure is very high. Recommend the patient to adhere to a low-sodium diet and stay hydrated. Provide medical intervention.")

    # Systolic BP
    if systolic_bp < 120:
        st.success("Patient's systolic blood pressure is normal.")
        

def analyze_cholesterol_physician(cholesterol):
    """
    Analyzes the cholesterol level of a patient and provides recommendations for a physician.

    Args:
        cholesterol (str): The cholesterol level of the patient.

    Notes:
        This function displays messages based on the cholesterol level and recommends appropriate actions for a physician.

    Recommendations:
        - If cholesterol level is normal, display a success message.
        - If cholesterol level is above normal, display a warning message and recommend a diet low in saturated fats and cholesterol, along with regular exercise.
        - If cholesterol level is well above normal, display an error message and recommend a diet low in saturated fats and cholesterol, regular exercise, and prescription of medication to manage cholesterol levels.
    """
    if cholesterol == "Normal":
        st.success("Patient's cholesterol level is normal.")
    elif cholesterol == "Above Normal":
        st.warning("Patient's cholesterol level is above normal. Recommend diet low in saturated fats and cholesterol. Suggest regular exercise.")
    else:
        st.error("Patient's cholesterol level is well above normal. Recommend diet low in saturated fats and cholesterol. Suggest regular exercise. Prescribe medication to manage cholesterol levels.")

def analyze_glucose_physician(glucose):
    """
    Analyzes the glucose level of a patient and provides recommendations for a physician.

    Args:
        glucose (str): The glucose level of the patient.

    Notes:
        This function displays messages based on the glucose level and recommends appropriate actions for a physician.

    Recommendations:
        - If glucose level is normal, display a success message.
        - If glucose level is above normal, display a warning message and recommend patient to reduce intake of sugary and high-carbohydrate foods, along with regular exercise.
        - If glucose level is well above normal, display an error message and recommend patient to reduce intake of sugary and high-carbohydrate foods, suggest regular exercise, and provide medical intervention.
    """
    if glucose == "Normal":
        st.success("Patient's glucose level is normal.")
    elif glucose == "Above Normal":
        st.warning("Patient's glucose level is above normal. Recommend patient to reduce intake of sugary and high-carbohydrate foods. Suggest regular exercise.")
    else:
        st.error("Patient's glucose level is well above normal. Recommend patient to reduce intake of sugary and high-carbohydrate foods. Suggest regular exercise. Provide medical intervention.")


def physician_page(user_id):
    """
    Displays the physician dashboard and allows updating patient information and predicting cardiovascular disease risk.

    Args:
        user_id (str): The ID of the logged-in physician.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    st.title("Physician Dashboard")
    st.write("Type to search and select a patient to update their information and see the risk of cardiovascular disease.")

    # Fetch all patients assigned to the logged-in physician
    cur.execute("""SELECT p."User ID", p."First Name", p."Last Name"
                   FROM patient p JOIN physicianpatientlink pl ON p."User ID" = pl."Patient ID"
                   WHERE pl."Physician ID" = %s""", (user_id,))
    patients = cur.fetchall()

    # Store patients in a dictionary for easier access
    patient_dict = {f"{patient[1]} {patient[2]}": patient[0] for patient in patients}

    # Input for dynamic search
    search_query = st.text_input("Search for a patient by name")

    # Filter patients as per the search query
    filtered_names = [name for name in patient_dict.keys() if search_query.lower() in name.lower()]

    # Selectbox with filtered options
    selected_name = st.selectbox("Select a Patient", filtered_names, key="patient_select")
    # Get the details of the selected patient
    if selected_name:
        patient_id = patient_dict[selected_name]
        cur.execute("""SELECT p."First Name", p."Last Name", p."age", p."gender", p."height", p."weight", 
               p."Smoke History", p."Alcohol Consumption", p."Exercise Level", m."Diastolic Blood Pressure", 
               m."Systolic Blood Pressure", m."cholesterol", m."glucose"
               FROM patient p 
               JOIN medicaltest m ON p."User ID" = m."Patient ID" 
               WHERE m."Patient ID" = %s""", (patient_id,))
        patient_info = cur.fetchone()

        if patient_info:
            with st.form(key='patient_details_form'):
                age = st.number_input("Age", value=patient_info[2])
                gender = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(convert_number_to_gender(patient_info[3])))
                height = st.number_input("Height (in cm)", value=patient_info[4])
                weight = st.number_input("Weight (in kg)", value=float(patient_info[5]), format="%.2f")
                smoke_history = st.selectbox("Smoke History", ["Yes", "No"], index=convert_to_number(patient_info[6]))
                alcohol_consumption = st.selectbox("Alcohol Consumption", ["Yes", "No"], index=convert_to_number(patient_info[7]))
                exercise_level = st.selectbox("Exercise Regularly", ["Yes", "No"], index=convert_to_number(patient_info[8]))
                diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=200, value=int(patient_info[9]))
                systolic_bp = st.number_input("Systolic Blood Pressure", min_value=70, max_value=300, value=int(patient_info[10]))
                cholesterol = st.selectbox("Cholesterol", bp_options, index=get_index_from_level(patient_info[11], bp_options))
                glucose = st.selectbox("Glucose", bp_options, index=get_index_from_level(patient_info[12], bp_options))# Additional fields can be displayed and edited here

                submit_button = st.form_submit_button("Update Patient Information and Predict Cardiovascular Results")

                if submit_button:
                    feature_array = np.array([[convert_gender_to_number(gender), height, weight, systolic_bp, diastolic_bp,  
                                                   convert_level_to_number(cholesterol), convert_level_to_number(glucose),
                                                   convert_to_number(smoke_history), convert_to_number(alcohol_consumption), convert_to_number(exercise_level), age]
                                                  ]).reshape(1, -1)
                    prediction = model.predict(feature_array)
                    cur.execute("""
                            UPDATE patient SET "age" = %s, "gender" = %s, "height" = %s, "weight" = %s,
                            "Smoke History" = %s, "Alcohol Consumption" = %s, "Exercise Level" = %s
                            WHERE "User ID" = %s
                        """, (int(age), int(convert_gender_to_number(gender)), int(height), float(weight),
          convert_to_number(smoke_history), convert_to_number(alcohol_consumption), convert_to_number(exercise_level), int(patient_id)))
                        
                        # Update current medical record
                    cur.execute("""
                            UPDATE medicaltest SET "Diastolic Blood Pressure"= %s, "Systolic Blood Pressure"= %s, "cholesterol"= %s, "glucose"= %s, "Cardiovascular Disease"= %s
                            WHERE "Patient ID" = %s
                        """, (int(diastolic_bp), int(systolic_bp), int(convert_level_to_number(cholesterol)), int(convert_level_to_number(glucose)), int(prediction[0]), int(patient_id)))
                    conn.commit()
                        
                    if prediction[0] == 1:
                        st.write('# Cardiovascular Disease Prediction:')
                        st.error(f"Based on patient's information, the patient is at high risk of cardiovascular disease. Medical assistance is advised.")
                        st.write('# Recommendations Based on Patient Information:')
                    else:
                        st.write('# Cardiovascular Disease Prediction:')
                        st.success(f"Based on patient's information, the patient is not at risk of cardiovascular disease.")
                        st.write('# Recommendations Based on Patient Information:')

                        # Additional health recommendations as per previous message
                    st.write('### Body Mass Index:')
                    bmi = weight / ((height / 100) ** 2)
                    if bmi >= 25:
                        st.warning(f"The patient's body mass index is {bmi:.1f}. Suggest weight loss measures to mitigate the risk of cardiovascular diseases.")
                    else:
                        st.success(f"The patient's body mass index is normal.")
                        # Blood Pressure Analysis
                    st.write('### Diastolic & Systolic Blood Pressure:')
                    analyze_blood_pressure_physician(diastolic_bp, systolic_bp)
                        # Cholesterol and Glucose Analysis
                    analyze_cholesterol_physician(cholesterol)
                    st.write('### Glucose Level:')
                    analyze_glucose_physician(glucose)
                    
                    st.write('### Life Style:')
                        # Lifestyle Recommendations
                    if smoke_history == "Yes":
                        st.warning("Recommend the patient discontinues smoking to enhance their overall health and diminish the risk of cardiovascular disease.")
                    else:
                        st.success("Patient is not smoking.")
                    if alcohol_consumption == "Yes":
                        st.warning("Advise the patient to decrease or discontinue alcohol consumption.")
                    else:
                        st.success("Patient is not consuming alcohol.")
                    if exercise_level == "No":
                        st.info("Recommend the patient to enegage in regular exerice, a minimum of three times per week.")
                    else:
                        st.success("Patient is exercising regularly.")
                    
                    st.write('### Information Update Confirmation:')
                    st.success("Patient information updated successfully.")

    cur.close()
    conn.close()


def patient_page(user_id):
    """
    Displays the patient dashboard and allows updating patient information, predicting cardiovascular disease risk, and providing health suggestions.

    Args:
        user_id (str): The ID of the logged-in patient.
    """
    st.title("Patient Dashboard")
    st.write("Welcome to your dashboard! Experiment by adjusting your information below and see the cardiovascular disease risk and health suggestions.")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT "First Name", "Last Name", "age", "gender", "Contact Information", "height", "weight", "Smoke History", "Alcohol Consumption", "Exercise Level", "Diastolic Blood Pressure", "Systolic Blood Pressure", "cholesterol", "glucose" FROM users u JOIN patient p ON u."User ID" = p."User ID" JOIN medicaltest m ON p."User ID" = m."Patient ID" WHERE p."User ID"=%s""", (user_id,))
    patient_details = cur.fetchone()

    if not patient_details:
        st.error("An error occurred while fetching patient details.")
        return

    with st.form(key='patient_form'):
        st.write("## Patient Details")
        first_name = st.text_input("First Name", patient_details[0])
        last_name = st.text_input("Last Name", patient_details[1])
        age = st.number_input("Age", value=patient_details[2])
        gender = st.selectbox("Gender", options=["Male", "Female"], index=["Male", "Female"].index(convert_number_to_gender(patient_details[3])))
        contact_info = st.text_input("Email", patient_details[4])
        height = st.number_input("Height (in cm)", value=patient_details[5])
        weight = st.number_input("Weight (in kg)", value=float(patient_details[6]), format="%.2f")
        smoke_history = st.selectbox("Smoke History", ["Yes", "No"], index=convert_to_number(patient_details[7]))
        alcohol_consumption = st.selectbox("Alcohol Consumption", ["Yes", "No"], index=convert_to_number(patient_details[8]))
        exercise_level = st.selectbox("Exercise Regularly", ["Yes", "No"], index=convert_to_number(patient_details[9]))
        diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=200, value=int(patient_details[10]))
        systolic_bp = st.number_input("Systolic Blood Pressure", min_value=70, max_value=300, value=int(patient_details[11]))
        cholesterol = st.selectbox("Cholesterol", bp_options, index=get_index_from_level(patient_details[12], bp_options))
        glucose = st.selectbox("Glucose", bp_options, index=get_index_from_level(patient_details[13], bp_options))

        submit_button = st.form_submit_button(label='Check Cardiovascular Disease Risk and Get Health Suggestions')

        if submit_button:
            # Prepare data for standardization and prediction
            feature_array = np.array([
                [convert_gender_to_number(gender), height, weight, systolic_bp, diastolic_bp,  
                convert_level_to_number(cholesterol), convert_level_to_number(glucose),
                convert_to_number(smoke_history), convert_to_number(alcohol_consumption), convert_to_number(exercise_level), age]
            ]).reshape(1, -1)
            # Make prediction of result
            prediction = model.predict(feature_array)
            if prediction[0] == 1:
                st.write('# Cardiovascular Disease Prediction:')
                st.error(f"Based on your inputs, you are at high risk of cardiovascular disease, please seek professional medical help.")
                st.write('# Recommendations Based on Your Input:')
            else:
                st.write('# Cardiovascular Disease Prediction:')
                st.success(f"Based on your inputs, you are not at risk of cardiovascular disease. Keep it up!")
                st.write('# Recommendations Based on Your Input:')

            # Additional health recommendations as per previous message
            st.write('### Body Mass Index:')
            bmi = weight / ((height / 100) ** 2)
            if bmi >= 25:
                st.warning(f"Your Body Mass Index is {bmi:.1f}. It's recommended to lose weight to lower your risk of cardiovascular disease.")
            else:
                st.success(f"Your Body Mass Index is normal. Keep it up!")
            
            st.write('### Diastolic & Systolic Blood Pressure:')
            # Blood Pressure Analysis
            analyze_blood_pressure(diastolic_bp, systolic_bp)
            
            st.write('### Cholesterol Level:')
            # Cholesterol and Glucose Analysis
            analyze_cholesterol(cholesterol)
            
            st.write('### Glucose Level:')
            analyze_glucose(glucose)
            
            st.write('### Life Style:')
            # Lifestyle Recommendations
            if smoke_history == "Yes":
                st.warning("It is strongly advised to stop smoking to improve your overall health and lower your risk of cardiovascular disease.")
            else:
                st.success("Opting not to smoke can lead to better health outcomes and a higher quality of life. Keep it up!")
            if alcohol_consumption == "Yes":
                st.warning("Consider reducing your alcohol intake to lower your health risks and lower your risk of cardiovascular disease.")
            else:
                st.success("Choosing not to consume alcohol can support your overall health and well-being, promoting clarity of mind and a healthier lifestyle. Keep it up!")
            if exercise_level == "No":
                st.info("Regular exercise is recommended. Try to exercise at least 3 times a week.")
            else:
                st.success("Engaging in regular exercise can significantly enhance your physical fitness, mental well-being, and overall quality of life. Keep it up!")

    cur.close()
    conn.close()


def register_user():
    """
    Allows registration of a new user from the sidebar.

    Notes:
        This function displays a form in the sidebar to register a new user.
        It checks if the entered username already exists and inserts the new user into the database if it doesn't exist.

    """
    st.sidebar.title("Register New User")
    with st.sidebar.form("register_form"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_user_type = st.selectbox("User Type", ["patient", "physician"])
        submit_button = st.form_submit_button("Register")

        if submit_button:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                # Check if username already exists
                cur.execute("SELECT * FROM users WHERE username = %s", (new_username,))
                if cur.fetchone() is not None:
                    st.sidebar.error("Username already exists. Try another username.")
                else:
                    # Insert new user into the database
                    cur.execute("INSERT INTO users (username, password, \"User Type\") VALUES (%s, %s, %s)",
                                (new_username, new_password, new_user_type))
                    conn.commit()
                    st.sidebar.success("User registered successfully!")
            except Exception as e:
                st.sidebar.error(f"An error occurred: {e}")
            finally:
                cur.close()
                conn.close()


def set_bg_from_url(url, opacity=1):
    """
    Sets the background of the app using the provided URL.

    Args:
        url (str): The URL of the image to be set as background.
        opacity (float, optional): The opacity level of the background image. Defaults to 1.

    """
    # HTML footer containing social media links
    footer = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <footer>
        <div style='visibility: visible;margin-top:7rem;justify-content:center;display:flex;'>
            <p style="font-size:1.1rem;">
                &nbsp;
                <a href="https://www.linkedin.com/in/huatingsun">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-linkedin" viewBox="0 0 16 16">
                        <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>          
                </a>
                &nbsp;
                <a href="https://github.com/PaulHuatingSun">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-github" viewBox="0 0 16 16">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                </a>
            </p>
        </div>
    </footer>
"""
    # Inject HTML footer
    st.markdown(footer, unsafe_allow_html=True)
    
    # Set background image using HTML and CSS
    st.markdown(
        f"""
        <style>
            body {{
                background: url('{url}') no-repeat center center fixed;
                background-size: cover;
                opacity: {opacity};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    """
    Main function to set up the Streamlit layout, including background image, login/register functionality, and user-specific pages.
    """
    # Set a background image from a URL with custom opacity
    set_bg_from_url("https://images.everydayhealth.com/homepage/health-topics-2.jpg?w=768", opacity=0.875)

    # Title and description
    st.title('Welcome to Cardiovascular Disease Decision Support System')
    st.write("Please utilize this Decision Support System to identify the likelihood of cardiovascular disease and recommend preventive actions")
    
    st.sidebar.title("User Login/Sign Up")

    # Radio button for user to select either Login or Register
    mode = st.sidebar.radio("Choose mode:", ["Login", "Register"])

    if mode == "Login":
        # Login section
        if 'user_id' not in st.session_state or 'user_type' not in st.session_state:
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")

            if st.sidebar.button("Login"):
                user_info = authenticate_user(username, password)
                if user_info:
                    st.session_state['user_id'], st.session_state['user_type'] = user_info
                    st.write(f"Logged in as {user_info[1]}")
                else:
                    st.sidebar.error("Invalid username or password")
    
    elif mode == "Register":
        # Registration section
        register_user()

    # Check if user is logged in
    if 'user_id' in st.session_state and 'user_type' in st.session_state:
        # Show a logout button in the sidebar
        if st.sidebar.button("Logout"):
            # Clear the session state when the user clicks logout
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.sidebar.success("You have been logged out.")
            # Refresh the page to return to login/register selection
            st.experimental_rerun()

        # Display the appropriate page based on user type
        if st.session_state['user_type'] == 'patient':
            patient_page(st.session_state['user_id'])
        elif st.session_state['user_type'] == 'physician':
            physician_page(st.session_state['user_id'])
        else:
            st.sidebar.error(f"Unhandled user type: {st.session_state['user_type']}")
    else:
        st.sidebar.write("Please log in or register to continue.")

if __name__ == "__main__":
    main()
