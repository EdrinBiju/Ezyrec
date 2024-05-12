from flask import Flask, request, jsonify, session, send_file 
from flask_cors import CORS 
from pymongo import MongoClient

import bcrypt
import requests
from fpdf import FPDF

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'your_secret_key'  # Change this to a secure key in production
client = MongoClient('mongodb://localhost:27017/')
db = client['university']

# Route for student login
@app.route('/student/login', methods=['POST'])
def student_login():
    login_data = request.json
    student = db.students.find_one({'register_no': login_data.get('register_no')})
    if student and bcrypt.checkpw(login_data.get('password').encode('utf-8'), student['password'].encode('utf-8')):
        session['student_id'] = student['register_no']
        individual_result = fetch_individual_result(student['register_no'])
        if individual_result:
            return jsonify({'message': 'Student logged in successfully', 'individual_result': individual_result})
        else:
            return jsonify({'message': 'Student logged in successfully', 'individual_result': 'Result not available'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

def fetch_individual_result(register_no):
    try:
        # Fetch individual result from the university website (replace 'url_to_result' with the actual URL)
        result_response = requests.get(f'https://api.ktu.edu.in/ktu-web-service/anon/individualresult/{register_no}')
        individual_result = result_response.json()  # Assuming the response is in JSON format
        return individual_result
    except Exception as e:
        print("Error fetching individual result:", str(e))
        return None

# Route for student logout
@app.route('/student/logout', methods=['POST'])
def student_logout():
    session.pop('student_id', None)
    return jsonify({'message': 'Student logged out successfully'})

# Route for faculty login
@app.route('/faculty/login', methods=['POST'])
def faculty_login():
    login_data = request.json
    faculty = db.faculty.find_one({'faculty_id': login_data.get('faculty_id')})
    if faculty and bcrypt.checkpw(login_data.get('password').encode('utf-8'), faculty['password'].encode('utf-8')):
        session['faculty_id'] = faculty['faculty_id']
        return jsonify({'message': 'Faculty logged in successfully'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Route for faculty logout
@app.route('/faculty/logout', methods=['POST'])
def faculty_logout():
    session.pop('faculty_id', None)
    return jsonify({'message': 'Faculty logged out successfully'})

# Routes for Students
@app.route('/students', methods=['GET'])
def get_students():
    students = list(db.students.find({}, {'_id': 0, 'password': 0}))
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    student_data = request.json
    # Validate student data before insertion
    if 'name' not in student_data or 'register_no' not in student_data:
        return jsonify({'error': 'Name and register number are required'}), 400
    # Hash and salt password for security
    hashed_password = bcrypt.hashpw(student_data.get('password').encode('utf-8'), bcrypt.gensalt())
    student_data['password'] = hashed_password.decode('utf-8')
    try:
        db.students.insert_one(student_data)
        return jsonify({'message': 'Student added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes for Faculty
@app.route('/faculty', methods=['GET'])
def get_faculty():
    faculty = list(db.faculty.find({}, {'_id': 0, 'password': 0}))
    return jsonify(faculty)

@app.route('/faculty', methods=['POST'])
def add_faculty():
    faculty_data = request.json
    # Validate faculty data before insertion
    if 'name' not in faculty_data or 'faculty_id' not in faculty_data:
        return jsonify({'error': 'Name and faculty ID are required'}), 400
    # Hash and salt password for security
    hashed_password = bcrypt.hashpw(faculty_data.get('password').encode('utf-8'), bcrypt.gensalt())
    faculty_data['password'] = hashed_password.decode('utf-8')
    try:
        db.faculty.insert_one(faculty_data)
        return jsonify({'message': 'Faculty added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for Certificates
@app.route('/verify_certificate/<certificate_id>', methods=['GET'])
def verify_certificate(certificate_id):
    certificate = db.certificates.find_one({'certificate_id': certificate_id})
    if not certificate:
        return jsonify({'error': 'Certificate not found'}), 404
    faculty_id = certificate.get('verified_by')
    faculty = db.faculty.find_one({'faculty_id': faculty_id}, {'_id': 0, 'password': 0})  # Exclude password
    if not faculty:
        return jsonify({'error': 'Faculty not found'}), 404
    
    # Generate PDF certificate
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in certificate.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")
    certificate_pdf_path = f"certificates/{certificate_id}.pdf"
    pdf.output(certificate_pdf_path)
    
    # Send the PDF file as an attachment
    return send_file(certificate_pdf_path, as_attachment=True)

# Route to fetch and store university results
@app.route('/fetch_results', methods=['GET'])
def fetch_results():
    try:
        # Fetch results from the university website (replace 'url_to_results' with the actual URL)
        results_response = requests.get('https://api.ktu.edu.in/ktu-web-service/anon/individualresult')
        results_data = results_response.json()  # Assuming the response is in JSON format

        # Store results in the database
        db.results.insert_many(results_data)

        return jsonify({'message': 'Results fetched and stored successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to fetch and store university notifications
@app.route('/fetch_notifications', methods=['GET'])
def fetch_notifications():
    try:
        # Fetch notifications from the university website (replace 'url_to_notifications' with the actual URL)
        notifications_response = requests.get('https://api.ktu.edu.in/ktu-web-portal-api/anon/announcemnts')
        notifications_data = notifications_response.json()  # Assuming the response is in JSON format

        # Store notifications in the database
        db.notifications.insert_many(notifications_data)

        return jsonify({'message': 'Notifications fetched and stored successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
