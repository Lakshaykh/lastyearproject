from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import psycopg2
from fpdf import FPDF
import mysql.connector
import pandas as pd
import joblib
import io
from sklearn.preprocessing import LabelEncoder, StandardScaler


app = Flask(__name__)
CORS(app)

# ✅ Database Connection Function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="project",
            user="postgres",
            password="@Qwerty123@",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Database connection failed:", str(e))
        return None

# ✅ Home Route (Renders index.html)
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Route for Display Page (Renders display.html)
@app.route('/display')
def display():
    return render_template('display.html')

# ✅ Route for Adding Details (Renders add_details.html)
@app.route('/add_details')
def add_details():
    return render_template('add_details.html')


@app.route('/knownchances', methods=['GET', 'POST'])  # Allow GET and POST
def knownchances():
    if request.method == 'GET':
        return render_template('knownchances.html')  # Load the form page

    try:
        data = request.form

        # ✅ Debugging - Print received data
        print("Received Data:", data)

        # ✅ Database Connection
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor()

        # ✅ SQL Query
        sql = """INSERT INTO company_jobs (
                    company_name, job_role, salary_package, required_skills, 
                    eligibility_criteria, application_deadline
                ) VALUES (%s, %s, %s, %s, %s, %s)"""

        values = (
            data.get('companyName'), data.get('jobRole'), data.get('salary'),
            data.get('skills'), data.get('eligibility'), data.get('deadline')
        )

        cur.execute(sql, values)
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('student_id'))  # Redirect after insert

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ Route for Student ID Input Page (Renders student_id.html)
@app.route('/student_id')
def student_id():
    return render_template('student_id.html')

# ✅ Insert Student Details into Database
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        # 🔹 Try to get JSON or form data correctly
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # 🔹 Debugging - Print received data
        print("Received Data:", data)

        # ✅ Ensure database connection
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor()

        # ✅ Correct SQL query
        sql = """INSERT INTO student_details (
                    student_id, tenth_percentage, twelfth_percentage, undergraduate_gpa, 
                    number_of_backlogs, certifications_completed, internship_experience_months, 
                    technical_skills_count, projects_completed, soft_skills_rating, aptitude_test_score, 
                    mock_interview_score, hackathon_participation, volunteering_experience, 
                    extracurricular_rating, age, gender, location, placement_training_participation, 
                    interview_call_rates, preferred_role, previous_internship_offers, 
                    desired_salary_range, placement_offer, specialization_field, semester_trend, 
                    coding_competitions_participation, tech_stack_expertise, github_activity, 
                    leadership_skills_rating, emotional_intelligence_score, time_management_skills, 
                    resume_quality_score, alumni_network_engagement, languages_known, 
                    disability_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # ✅ Extract values properly
        values = (
    data.get('student_ID'), data.get('Tenth_Percentage', None), 
    data.get('Twelfth_Percentage', None), data.get('Undergraduate_GPA', None), 
    data.get('Number_of_Backlogs', None), data.get('Certifications_Completed', None), 
    data.get('Internship_Experience_Months', None), data.get('Technical_Skills_Count', None), 
    data.get('Projects_Completed', None), data.get('Soft_Skills_Rating', None), 
    data.get('Aptitude_Test_Score', None), data.get('Mock_Interview_Score', None), 
    data.get('Hackathon_Participation', None), data.get('Volunteering_Experience', None), 
    data.get('Extracurricular_Rating', None), data.get('Age', None), 
    data.get('Gender', None), data.get('Location', None), 
    data.get('Placement_Training_Participation', None), data.get('Interview_Call_Rates', None), 
    data.get('Preferred_Role', None), data.get('Previous_Internship_Offers', None), 
    data.get('Desired_Salary_Range', None), data.get('Placement_Offer', None), 
    data.get('Specialization_Field', None), data.get('Semester_Trend', None), 
    data.get('Coding_Competitions_Participation', None), data.get('Tech_Stack_Expertise', None), 
    data.get('GitHub_Activity', None), data.get('Leadership_Skills_Rating', None), 
    data.get('Emotional_Intelligence_Score', None), data.get('Time_Management_Skills', None), 
    data.get('Resume_Quality_Score', None), data.get('Alumni_Network_Engagement', None), 
    data.get('Languages_Known', None), data.get('Disability_Status', None)
)
        # 🔹 Debugging - Check query and values before execution
        print("Executing Query:", cur.mogrify(sql, values))

        # ✅ Execute the query
        cur.execute(sql, values)
        conn.commit()

        # ✅ Close database connection
        cur.close()
        conn.close()

        return jsonify({"message": "Student data inserted successfully!"}), 201

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500
    

# ✅ Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
