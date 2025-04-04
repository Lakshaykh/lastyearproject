import cgi
import mysql.connector

# Get form data from HTML
form = cgi.FieldStorage()

# Extract all values from form
data = {
    "Student_ID": form.getvalue("Student_ID"),
    "Tenth_Percentage": form.getvalue("Tenth_Percentage"),
    "Twelfth_Percentage": form.getvalue("Twelfth_Percentage"),
    "Undergraduate_GPA": form.getvalue("Undergraduate_GPA"),
    "Number_of_Backlogs": form.getvalue("Number_of_Backlogs"),
    "Certifications_Completed": form.getvalue("Certifications_Completed"),
    "Internship_Experience_Months": form.getvalue("Internship_Experience_Months"),
    "Technical_Skills_Count": form.getvalue("Technical_Skills_Count"),
    "Projects_Completed": form.getvalue("Projects_Completed"),
    "Soft_Skills_Rating": form.getvalue("Soft_Skills_Rating"),
    "Aptitude_Test_Score": form.getvalue("Aptitude_Test_Score"),
    "Mock_Interview_Score": form.getvalue("Mock_Interview_Score"),
    "Hackathon_Participation": form.getvalue("Hackathon_Participation"),
    "Volunteering_Experience": form.getvalue("Volunteering_Experience"),
    "Extracurricular_Rating": form.getvalue("Extracurricular_Rating"),
    "Age": form.getvalue("Age"),
    "Gender": form.getvalue("Gender"),
    "Location": form.getvalue("Location"),
    "Placement_Training_Participation": form.getvalue("Placement_Training_Participation"),
    "Interview_Call_Rates": form.getvalue("Interview_Call_Rates"),
    "Preferred_Role": form.getvalue("Preferred_Role"),
    "Previous_Internship_Offers": form.getvalue("Previous_Internship_Offers"),
    "Desired_Salary_Range": form.getvalue("Desired_Salary_Range"),
    "Placement_Offer": form.getvalue("Placement_Offer"),
    "Specialization_Field": form.getvalue("Specialization_Field"),
    "Semester_Trend": form.getvalue("Semester_Trend"),
    "Coding_Competitions_Participation": form.getvalue("Coding_Competitions_Participation"),
    "Tech_Stack_Expertise": form.getvalue("Tech_Stack_Expertise"),
    "GitHub_Activity": form.getvalue("GitHub_Activity"),
    "Leadership_Skills_Rating": form.getvalue("Leadership_Skills_Rating"),
    "Emotional_Intelligence_Score": form.getvalue("Emotional_Intelligence_Score"),
    "Time_Management_Skills": form.getvalue("Time_Management_Skills"),
    "Resume_Quality_Score": form.getvalue("Resume_Quality_Score"),
    "Alumni_Network_Engagement": form.getvalue("Alumni_Network_Engagement"),
    "Languages_Known": form.getvalue("Languages_Known"),
    "Disability_Status": form.getvalue("Disability_Status"),
    "Fathers_Occupation": form.getvalue("Fathers_Occupation")
}

# Connect to MySQL
conn = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12765915",
    password="ztDgECFwsd",
    database="sql12765915"
)
cursor = conn.cursor()

# Insert data into MySQL
query = """
INSERT INTO students (
    Student_ID, Tenth_Percentage, Twelfth_Percentage, Undergraduate_GPA, Number_of_Backlogs,
    Certifications_Completed, Internship_Experience_Months, Technical_Skills_Count, Projects_Completed,
    Soft_Skills_Rating, Aptitude_Test_Score, Mock_Interview_Score, Hackathon_Participation,
    Volunteering_Experience, Extracurricular_Rating, Age, Gender, Location, Placement_Training_Participation,
    Interview_Call_Rates, Preferred_Role, Previous_Internship_Offers, Desired_Salary_Range, Placement_Offer,
    Specialization_Field, Semester_Trend, Coding_Competitions_Participation, Tech_Stack_Expertise,
    GitHub_Activity, Leadership_Skills_Rating, Emotional_Intelligence_Score, Time_Management_Skills,
    Resume_Quality_Score, Alumni_Network_Engagement, Languages_Known, Disability_Status, Fathers_Occupation
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
values = tuple(data.values())

try:
    cursor.execute(query, values)
    conn.commit()
    message = "Data submitted successfully!"
except Exception as e:
    message = f"Error: {e}"

# Close connection
cursor.close()
conn.close()

# Print response
print("Content-Type: text/html\n")
print(f"<html><body><h2>{message}</h2></body></html>")
