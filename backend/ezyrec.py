from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_jwt_extended import JWTManager, create_access_token
from flask_pymongo import PyMongo
from datetime import timedelta, datetime, timezone
from flask_cors import CORS
import requests, smtplib, os, uuid, pyotp, datetime, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from activitypoint import CalculateActivityPoint
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId
from dateutil.relativedelta import relativedelta
import pymongo

app = Flask(__name__)
app.config['DEBUG'] = True  # Ensure the app is running in debug mode

# logging.basicConfig(level=logging.DEBUG)

# Configure MongoDB
# app.config["MONGO_URI"] = "mongodb://localhost:27017/ezyrec"  # Update with your database name
app.config['UPLOAD_FOLDER'] = 'uploads'
# mongo = PyMongo(app)
mongo = pymongo.MongoClient("mongodb+srv://testofunknown:Abc123@ezyrec-database.utsamq6.mongodb.net/?retryWrites=true&w=majority&appName=ezyrec-database")

if mongo:
    print("connected")
else: 
    print("not connected")
jwt = JWTManager(app)
CORS(app)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

def clean_user_data(user):
    user['_id'] = str(user['_id'])
    return user

@app.route('/studentlogin', methods=['POST'])
def student_login():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()

    if not data or not data.get('regno') or not data.get('password'):
        return jsonify({'error': 'reg_no and password are required'}), 400

    reg_no = data['regno']
    password = data['password']

    user = mongo.ezyrec.student.find_one({'reg_no': reg_no})

    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid reg_no or password'}), 401

    access_token = create_access_token(identity={'reg_no': reg_no})

    user = clean_user_data(user)

    return jsonify({'token': access_token, 'data': user}), 200

@app.route('/facultylogin', methods=['POST'])
def faculty_login():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()

    if not data or not data.get('facultyid') or not data.get('password'):
        return jsonify({'error': 'faculty_id and password are required'}), 400

    faculty_id = data['facultyid']
    password = data['password']

    user = mongo.ezyrec.faculty.find_one({'faculty_id': faculty_id})

    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid faculty_id or password'}), 401

    access_token = create_access_token(identity={'faculty_id': faculty_id})

    user = clean_user_data(user)

    return jsonify({'token': access_token, 'data': user}), 200

@app.route('/announcements', methods=['POST'])
def get_announcements():
    data = request.json
    apiUrl = 'https://api.ktu.edu.in/ktu-web-portal-api/anon/announcemnts'
    requestData = {
        "number": data.get("pageNumber", 0),
        "size": data.get("dataSize", 10),
        "searchText": data.get("searchText", "")
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Referer': 'https://ktu.edu.in/',
        'Origin': 'https://ktu.edu.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    try:
        # logging.debug('Sending POST request to KTU API')
        response = requests.post(apiUrl, json=requestData, headers=headers, verify=False)
        response.raise_for_status()

        jsonData = response.json()
        # logging.debug('Response received from KTU API')

        if jsonData and 'content' in jsonData:
            notifications = []
            for item in jsonData['content']:#[:10]:
                date = item['announcementDate']
                title = item['subject']
                description = item['message']
                attachmentList = item.get('attachmentList', [])
                links = [
                    {
                        'url_title': att['title'], 
                        'encryptId': att['encryptId']
                    } 
                    for att in attachmentList
                ]

                notifications.append({
                    'date': date,
                    'title': title,
                    'description': description,
                    'links': links
                })

            result = {
                'last_updated' : datetime.datetime.now(timezone.utc).isoformat() + 'Z',
                'is_ktusite_online': True,
                'notifications': notifications,
            }

            return jsonify(result)
        else:
            # logging.error('No content found in JSON data.')
            return jsonify({"message": "No content found"}), 204

    except requests.exceptions.RequestException as e:
        # logging.error(f"Request failed: {e}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        # logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

def generate_unique_filename(filename):
    unique_filename = str(uuid.uuid4()) + "_" + filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    while os.path.exists(file_path):
        unique_filename = str(uuid.uuid4()) + "_" + filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    return unique_filename, file_path

@app.route('/addcertificates', methods=['POST'])
def add_certificate():
    reg_no = request.form.get('reg_no')
    certificate_name = request.form.get('certificateName')
    organization = request.form.get('organization')
    issue_date = request.form.get('issueDate')
    criteria = request.form.get('criteria')
    sub_criteria = request.form.get('subCriteria')
    level = request.form.get('level')
    approval_document = request.form.get('approvalDocument')
    achievement = request.form.get('achievement')

    if achievement=="None Of The Above" or achievement=="Participation":
        achievement=""
    
    # Handling file upload
    certificate_file = request.files.get('certificateFile')
    if certificate_file:
        unique_filename, file_path = generate_unique_filename(certificate_file.filename)
        certificate_file.save(file_path)
    else:
        return jsonify({"error": "No file uploaded"}), 400
    if criteria == "National Initiatives" and achievement != "":
        achievement_file = request.files.get('achievementFile')
        achievement_filename = achievement_file.filename
        if achievement_file:
            achievement_unique_filename, achievement_file_path = generate_unique_filename(achievement_filename)
            achievement_file.save(achievement_file_path)
        else:
            return jsonify({"error": "No file uploaded"}), 400
    else: 
        achievement_filename = achievement_unique_filename = achievement_file_path = ""

    activity_point = CalculateActivityPoint(
        {
            "criteria": criteria,
            "subCriteria": sub_criteria,
            "level": level,
            "achievement": achievement
        }
    )

    student = mongo.ezyrec.student.find_one({'reg_no': reg_no})

    certificate = {
        "reg_no": reg_no,
        "student":student['name'],
        "certificateName": certificate_name,
        "organization": organization,
        "issueDate": issue_date,
        "criteria": criteria,
        "subCriteria": sub_criteria,
        "level": level,
        "approvalDocument": approval_document,
        "filePath": file_path,
        "originalFilename": certificate_file.filename,
        "uniqueFilename": unique_filename,
        "achievement": achievement,
        "achievementFilePath": achievement_file_path,
        "achievementOriginalFilename": achievement_filename,
        "achievementUniqueFilename": achievement_unique_filename,
        "activity_point": activity_point,
        "status": "Pending"
    }

    result = mongo.ezyrec.certificates.insert_one(certificate)
    return jsonify({"message": "Certificate added", "id": str(result.inserted_id)}), 201

@app.route('/view/uploads/<filename>')
def uploaded_file(filename):
    # Find the document with the unique filename
    document = mongo.ezyrec.certificates.find_one({"uniqueFilename": filename})
    if document:
        original_filename = document['originalFilename']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False, download_name=original_filename)
    else:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/viewAchievement/uploads/<filename>')
def uploadedd_file(filename):
    # Find the document with the unique filename
    document = mongo.ezyrec.certificates.find_one({"achievementUniqueFilename": filename})
    if document:
        original_filename = document['achievementOriginalFilename']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False, download_name=original_filename)
    else:
        return jsonify({"error": "File not found"}), 404
        
@app.route('/download/uploads/<filename>')
def uploadeddd_file(filename):
    # Find the document with the unique filename
    document = mongo.ezyrec.certificates.find_one({"uniqueFilename": filename})
    if document:
        original_filename = document['originalFilename']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, download_name=original_filename)
    else:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/downloadAchievement/uploads/<filename>')
def uploadedddd_file(filename):
    # Find the document with the unique filename
    document = mongo.ezyrec.certificates.find_one({"achievementUniqueFilename": filename})
    if document:
        original_filename = document['achievementOriginalFilename']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, download_name=original_filename)
    else:
        return jsonify({"error": "File not found"}), 404
    
@app.route("/studentcertificates", methods=["POST"])
def get_student_certificates():
    data = request.get_json()
    reg_no = data.get('reg_no')
    if not reg_no:
        return jsonify({"error": "Registration number is required"}), 400

    certificates = mongo.ezyrec.certificates.find({"reg_no": reg_no})

    serialized_certificates = []
    for certificate in certificates:
        serialized_certificate = {
            "certificate_name": certificate["certificateName"],
            "organization": certificate["organization"],
            "issue_date": certificate["issueDate"],
            "criteria": certificate["criteria"],
            "sub_criteria": certificate["subCriteria"],
            "level": certificate["level"],
            "achievement": certificate["achievement"],
            "approval_document": certificate["approvalDocument"],
            "file_path": certificate["filePath"],
            "original_filename": certificate["originalFilename"],
            "unique_filename": certificate["uniqueFilename"],
            "achievement_file_path": certificate["achievementFilePath"],
            "achievement_original_filename": certificate["achievementOriginalFilename"],
            "achievement_unique_filename": certificate["achievementUniqueFilename"],
            "activity_point": certificate["activity_point"],
            "status": certificate["status"],
            "id":str(certificate['_id'])
        }
        serialized_certificates.append(serialized_certificate)

    return jsonify({"certificates": serialized_certificates})

@app.route('/student/<reg_no>', methods=['GET'])
def get_student_profile(reg_no):
    student = mongo.ezyrec.student.find_one({'reg_no': reg_no})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    studentdata = {
        "reg_no":student["reg_no"],
        "name":student["name"],
        "dob":student["dob"],
        "gender":student["gender"],
        "department":student["department"],
        "email":student["email"],
        "profilePath":student["profilePath"],
        "activity_points":student["activity_points"]
    }
    return studentdata

@app.route('/faculty/<faculty_id>', methods=['GET'])
def get_faculty_profile(faculty_id):
    faculty = mongo.ezyrec.faculty.find_one({'faculty_id': faculty_id})
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404
    Facultydata = {
        "faculty_id":faculty["faculty_id"],
        "name":faculty["name"],
        "department":faculty["department"],
        "email":faculty["email"],
        "profilePath":faculty["profilePath"]
    }
    return Facultydata

@app.route('/addstudentprofile', methods=['POST'])
def add_student_profile():
    reg_no = request.form.get('reg_no')
    profile_pic = request.files.get('profilePic')

    if not profile_pic:
        return jsonify({"error": "No file uploaded"}), 400

    # Fetch the student's current profile to check if a profile picture already exists
    student = mongo.ezyrec.student.find_one({'reg_no': reg_no})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Remove the existing profile picture from the server if it exists
    existing_profile_path = student.get('profilePath')
    if existing_profile_path:
        if os.path.exists(existing_profile_path):
            os.remove(existing_profile_path)

    # Save the new profile picture
    unique_filename, file_path = generate_unique_filename(profile_pic.filename)
    profile_pic.save(file_path)

    # Update the MongoDB record with the new profile picture path
    result = mongo.ezyrec.student.update_one(
        {'reg_no': reg_no},
        {'$set': {'profilePath': file_path}}
    )

    if result.modified_count == 1:
        return jsonify({"message": "Profile picture updated successfully", "profilePath": file_path}), 200
    else:
        return jsonify({"error": "Failed to update profile picture"}), 500
    
@app.route('/addfacultyprofile', methods=['POST'])
def add_faculty_profile():
    faculty_id = request.form.get('faculty_id')
    profile_pic = request.files.get('profilePic')

    if not profile_pic:
        return jsonify({"error": "No file uploaded"}), 400

    # Fetch the student's current profile to check if a profile picture already exists
    faculty = mongo.ezyrec.faculty.find_one({'faculty_id': faculty_id})
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    # Remove the existing profile picture from the server if it exists
    existing_profile_path = faculty.get('profilePath')
    if existing_profile_path:
        if os.path.exists(existing_profile_path):
            os.remove(existing_profile_path)

    # Save the new profile picture
    unique_filename, file_path = generate_unique_filename(profile_pic.filename)
    profile_pic.save(file_path)

    # Update the MongoDB record with the new profile picture path
    result = mongo.ezyrec.faculty.update_one(
        {'faculty_id': faculty_id},
        {'$set': {'profilePath': file_path}}
    )

    if result.modified_count == 1:
        return jsonify({"message": "Profile picture updated successfully", "profilePath": file_path}), 200
    else:
        return jsonify({"error": "Failed to update profile picture"}), 500

@app.route('/profile/uploads/<filename>')
def fetch_profile(filename):
    # Find the document with the unique filename
    if filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
    else:
        return jsonify({"error": "File not found"}), 404
    
SECRET = pyotp.random_base32()

# OTP expiration time in seconds
OTP_EXPIRATION = 300  # 5 minutes

def send_otp_email(to_email, otp):
    with app.app_context():  # Push the application context
        from_email = "ezyrecbot@outlook.com"
        from_password = "f123f456"

        subject = "Your OTP Code"
        body = render_template('email_template.html', otp=otp)

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp.outlook.com', 587)
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")

@app.route('/request-otp', methods=['POST'])
def request_otp():
    data = request.json
    reg_no = data.get('reg_no')
    new_email = data.get('new_email')
    if not reg_no or not new_email:
        return jsonify({"error": "Student ID and new email are required"}), 400

    student = mongo.ezyrec.student.find_one({"reg_no": reg_no})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    totp = pyotp.TOTP(SECRET)
    otp = totp.now()
    # Save OTP and its expiration time in the database
    otp_record = {
        "reg_no": reg_no,
        "new_email": new_email,
        "otp": otp,
        "expires_at": (datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=OTP_EXPIRATION)).astimezone(timezone.utc)
    }
    mongo.ezyrec.otp.insert_one(otp_record)

    email_thread = threading.Thread(target=send_otp_email, args=(new_email, otp))
    email_thread.start()

    return jsonify({"message": "OTP sent to new email"}), 200
    # Send OTP to the new email
    # if send_otp_email(new_email, otp):
    #     return jsonify({"message": "OTP sent to new email"}), 200
    # else:
    #     return jsonify({"error": "Failed to send OTP to new email"}), 500

@app.route('/request-otp-faculty', methods=['POST'])
def request_otp_faculty():
    data = request.json
    faculty_id = data.get('faculty_id')
    new_email = data.get('new_email')
    if not faculty_id or not new_email:
        return jsonify({"error": "Student ID and new email are required"}), 400

    faculty = mongo.ezyrec.faculty.find_one({"faculty_id": faculty_id})
    if not faculty:
        return jsonify({"error": "Student not found"}), 404

    totp = pyotp.TOTP(SECRET)
    otp = totp.now()
    # Save OTP and its expiration time in the database
    otp_record = {
        "faculty_id": faculty_id,
        "new_email": new_email,
        "otp": otp,
        "expires_at": (datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=OTP_EXPIRATION)).astimezone(timezone.utc)
    }
    mongo.ezyrec.otp.insert_one(otp_record)

    email_thread = threading.Thread(target=send_otp_email, args=(new_email, otp))
    email_thread.start()

    return jsonify({"message": "OTP sent to new email"}), 200

@app.route('/update-email', methods=['POST'])
def update_email():
    data = request.json  # Ensure correct parsing of JSON data
    reg_no = data.get('reg_no')
    new_email = data.get('new_email')
    otp = data.get('otp')

    if not all([reg_no, new_email, otp]):
        return jsonify({"error": "Student ID, new email, and OTP are required"}), 400

    # Verify OTP
    otp_record = mongo.ezyrec.otp.find_one({"reg_no": reg_no, "new_email": new_email, "otp": otp})
    if not otp_record:
        return jsonify({"error": "Invalid OTP"}), 400

    # Convert expires_at to a timezone-aware datetime object
    expires_at = otp_record["expires_at"]
    expires_at = expires_at.replace(tzinfo=timezone.utc)
    # Convert current time to a timezone-aware datetime object
    current_time = datetime.datetime.now(timezone.utc)
    current_time = current_time.astimezone(timezone.utc)

    # Check if the OTP has expired
    if expires_at < current_time:
        return jsonify({"error": "OTP has expired"}), 400

    # Update the student's email in the database
    mongo.ezyrec.student.update_one({"reg_no": reg_no}, {"$set": {"email": new_email}})

    # Delete the OTP record after successful verification
    mongo.ezyrec.otp.delete_one({"_id": otp_record["_id"]})

    return jsonify({"message": "Email updated successfully"}), 200

@app.route('/update-email-faculty', methods=['POST'])
def update_email_faculty():
    data = request.json  # Ensure correct parsing of JSON data
    faculty_id = data.get('faculty_id')
    new_email = data.get('new_email')
    otp = data.get('otp')

    if not all([faculty_id, new_email, otp]):
        return jsonify({"error": "Student ID, new email, and OTP are required"}), 400

    # Verify OTP
    otp_record = mongo.ezyrec.otp.find_one({"faculty_id": faculty_id, "new_email": new_email, "otp": otp})
    if not otp_record:
        return jsonify({"error": "Invalid OTP"}), 400

    # Convert expires_at to a timezone-aware datetime object
    expires_at = otp_record["expires_at"]
    expires_at = expires_at.replace(tzinfo=timezone.utc)
    # Convert current time to a timezone-aware datetime object
    current_time = datetime.datetime.now(timezone.utc)
    current_time = current_time.astimezone(timezone.utc)

    # Check if the OTP has expired
    if expires_at < current_time:
        return jsonify({"error": "OTP has expired"}), 400

    # Update the student's email in the database
    mongo.ezyrec.faculty.update_one({"faculty_id": faculty_id}, {"$set": {"email": new_email}})

    # Delete the OTP record after successful verification
    mongo.ezyrec.otp.delete_one({"_id": otp_record["_id"]})

    return jsonify({"message": "Email updated successfully"}), 200

@app.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.json
    reg_no = data.get('reg_no')
    current_password = data.get('current_password')
    
    if not reg_no or not current_password:
        return jsonify({"error": "Username and current password are required"}), 400

    user = mongo.ezyrec.student.find_one({"reg_no": reg_no})

    if not user or (user['password'] != current_password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Password verified successfully"}), 200

@app.route('/verify-password-faculty', methods=['POST'])
def verify_password_faculty():
    data = request.json
    faculty_id = data.get('faculty_id')
    current_password = data.get('current_password')
    
    if not faculty_id or not current_password:
        return jsonify({"error": "Username and current password are required"}), 400

    user = mongo.ezyrec.faculty.find_one({"faculty_id": faculty_id})

    if not user or (user['password'] != current_password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Password verified successfully"}), 200

@app.route('/change-password', methods=['POST'])
def change_password():
    data = request.json
    reg_no = data.get('reg_no')
    new_password = data.get('new_password')
    print(reg_no,new_password)
    if not reg_no or not new_password:
        return jsonify({"error": "Username and new password are required"}), 400

    # user = mongo.db.student.find_one({"reg_no": reg_no})
    # if not user or (user['password'] != current_password):
    #     return jsonify({"error": "Invalid username or current password"}), 401

    mongo.ezyrec.student.update_one({"reg_no": reg_no}, {"$set": {"password": new_password}})

    return jsonify({"message": "Password changed successfully"}), 200

@app.route('/change-password-faculty', methods=['POST'])
def change_password_faculty():
    data = request.json
    faculty_id = data.get('faculty_id')
    new_password = data.get('new_password')
    print(faculty_id,new_password)
    if not faculty_id or not new_password:
        return jsonify({"error": "Username and new password are required"}), 400

    # user = mongo.db.student.find_one({"reg_no": reg_no})
    # if not user or (user['password'] != current_password):
    #     return jsonify({"error": "Invalid username or current password"}), 401

    mongo.ezyrec.faculty.update_one({"faculty_id": faculty_id}, {"$set": {"password": new_password}})

    return jsonify({"message": "Password changed successfully"}), 200

@app.route('/certificates', methods=['POST'])
def get_certificates():
    status = request.form.get('status')
    category = request.form.get('category')
    search_text = request.form.get('searchText')
    
    query = {}
    
    if status and status != "All":
        query['status'] = status
    
    if category == "All Students":
        pass  # No additional query needed for this category
    elif category == "Search By Name" and search_text:
        query['student'] = {'$regex': search_text, '$options': 'i'}
    elif category == "Search By Register Number" and search_text:
        query['reg_no'] = {'$regex': search_text, '$options': 'i'}
    
    certificates = mongo.ezyrec.certificates.find(query)
    
    serialized_certificates = []
    for certificate in certificates:
        serialized_certificate = {
            "student":certificate['student'],
            "reg_no":certificate['reg_no'],
            "certificate_name": certificate["certificateName"],
            "organization": certificate["organization"],
            "issue_date": certificate["issueDate"],
            "criteria": certificate["criteria"],
            "sub_criteria": certificate["subCriteria"],
            "level": certificate["level"],
            "achievement": certificate["achievement"],
            "approval_document": certificate["approvalDocument"],
            "file_path": certificate["filePath"],
            "original_filename": certificate["originalFilename"],
            "unique_filename": certificate["uniqueFilename"],
            "achievement_file_path": certificate["achievementFilePath"],
            "achievement_original_filename": certificate["achievementOriginalFilename"],
            "achievement_unique_filename": certificate["achievementUniqueFilename"],
            "activity_point": certificate["activity_point"],
            "status": certificate["status"],
            "id":str(certificate['_id'])
        }
        serialized_certificates.append(serialized_certificate)
    return jsonify({"certificates": serialized_certificates})

@app.route('/certificates/<certificate_id>', methods=['DELETE'])
def delete_certificate(certificate_id):
    try:
        # Ensure the ID is a valid ObjectId
        if not ObjectId.is_valid(certificate_id):
            return jsonify({"error": "Invalid certificate ID"}), 400

        # Convert string to ObjectId
        object_id = ObjectId(certificate_id)
        
        # Find the certificate by ID
        certificate = mongo.ezyrec.certificates.find_one({"_id": object_id})
        if not certificate:
            return jsonify({"error": "Certificate not found"}), 404

        # Delete the certificate file from the folder
        file_path = certificate.get('filePath')
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        # Subtract activity points if the status is "Accepted"
        if certificate['status'] == 'Accepted':
            reg_no = certificate['reg_no']
            student = mongo.ezyrec.student.find_one({"reg_no": reg_no})
            if student:
                new_points = student['activity_points'] - certificate['activity_point']
                mongo.ezyrec.student.update_one({"reg_no": reg_no}, {"$set": {"activity_points": new_points}})
        
        # Delete the certificate from the MongoDB collection
        mongo.ezyrec.certificates.delete_one({"_id": object_id})

        return jsonify({"message": "Certificate deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/reject/<certificate_id>', methods=['POST'])
def reject_certificate(certificate_id):
    try:
        if not ObjectId.is_valid(certificate_id):
            return jsonify({"error": "Invalid certificate ID"}), 400

        _id = ObjectId(certificate_id)
        certificate = mongo.ezyrec.certificates.find_one({"_id": _id})
        if not certificate:
            return jsonify({"error": "Certificate not found"}), 404
        
        if certificate['status'] == 'Accepted':
            reg_no = certificate['reg_no']
            student = mongo.ezyrec.student.find_one({"reg_no": reg_no})
            if student:
                new_points = student['activity_points'] - certificate['activity_point']
                mongo.ezyrec.student.update_one({"reg_no": reg_no}, {"$set": {"activity_points": new_points}})

        mongo.ezyrec.certificates.update_one({"_id": _id}, {"$set": {"status": "Rejected"}})
        return jsonify({"message": "Certificate rejected successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/accept/<certificate_id>', methods=['POST'])
def accept_certificate(certificate_id):
    try:
        if not ObjectId.is_valid(certificate_id):
            return jsonify({"error": "Invalid certificate ID"}), 400

        _id = ObjectId(certificate_id)
        certificate = mongo.ezyrec.certificates.find_one({"_id": _id})
        if not certificate:
            return jsonify({"error": "Certificate not found"}), 404

        reg_no = certificate.get('reg_no')
        activity_points = certificate.get('activity_point', 0)
        if not reg_no:
            return jsonify({"error": "Student registration number not found in certificate"}), 400

        student = mongo.ezyrec.student.find_one({"reg_no": reg_no})
        if not student:
            return jsonify({"error": "Student not found"}), 404

        current_points = student.get('activity_points', 0)
        new_points = current_points + activity_points

        mongo.ezyrec.student.update_one({"reg_no": reg_no}, {"$set": {"activity_points": new_points}})
        mongo.ezyrec.certificates.update_one({"_id": _id}, {"$set": {"status": "Accepted"}})

        return jsonify({"message": "Certificate accepted and activity points added"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
OFFICIAL_API_RESULTS_URL = 'https://api.ktu.edu.in/ktu-web-service/anon/result'
OFFICIAL_API_INDIVIDUAL_RESULT_URL = 'https://api.ktu.edu.in/ktu-web-service/anon/individualresult'

# Example payload for all published results
PUBLISHED_RESULTS_PAYLOAD = {
    "program": ""
}

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Referer': 'https://ktu.edu.in/',
    'Origin': 'https://ktu.edu.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

@app.route('/fetch-published-results', methods=['GET'])
def fetch_published_results():
    try:
        # Fetch the list of all published results from the official API
        response = requests.post(OFFICIAL_API_RESULTS_URL, json=PUBLISHED_RESULTS_PAYLOAD, headers=HEADERS, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        all_published_results = response.json()
        btech_published_results = []
        for result in all_published_results:
            if "b.tech" in result['resultName'].lower() or "btech" in result['resultName'] :
                btech_published_results.append(result)
        return jsonify(btech_published_results), 200
    except requests.exceptions.RequestException as e:
        print(f"Error fetching published results: {e}")
        return jsonify({"error": "Failed to fetch published results"}), 500

@app.route('/fetch-student-result', methods=['GET'])
def fetch_student_result():
    print("Request received for /published-results-student")
    response = requests.post(OFFICIAL_API_RESULTS_URL, json=PUBLISHED_RESULTS_PAYLOAD, headers=HEADERS, verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors

    all_published_results = response.json()
    btech_published_results = []
    for result in all_published_results:
        if "b.tech" in result['resultName'].lower() or "btech" in result['resultName'].lower() :
            btech_published_results.append(result)
    # print(btech_published_results)
    for p_result in btech_published_results:
        token = p_result['token']
        published_date = datetime.datetime.strptime(p_result['publishDate'], "%Y-%m-%d")
        resultName = p_result['resultName']

        if not token:
            continue

        try:
            students = mongo.ezyrec.student.find()

            for student in students:

                join_date = student.get('join_date')
                if join_date:
                    join_date = datetime.datetime.strptime(str(join_date), "%Y-%m-%d %H:%M:%S")
                else:
                    continue  # Skip if no join_date

                join_date_plus_4_months = join_date + relativedelta(months=+4)
                if published_date <= join_date_plus_4_months:
                    continue  # Skip if published date is not greater than join date + 4 months

                register_no = student.get('reg_no')
                date_st = student['dob']
                date_st = datetime.datetime.strptime(str(date_st), "%Y-%m-%d %H:%M:%S")
                date_of_birth = str(date_st.strftime("%Y-%m-%d"))

                # Check if the result for this student and token already exists in MongoDB
                existing_result = mongo.ezyrec.results.find_one({"reg_no": register_no, "result_name": resultName})
                if existing_result:
                    continue  # Skip if already exists

                # Fetch individual student result
                payload = {
                    "dateOfBirth": date_of_birth,
                    "registerNo": register_no,
                    "token": token
                }
                try:
                    student_response = requests.post(OFFICIAL_API_INDIVIDUAL_RESULT_URL, json=payload, headers=HEADERS, verify=False)
                    student_response.raise_for_status()
                    student_result = student_response.json()

                    if student_result['resultDetails'] is None:
                        validity = "Invalid"
                    else:
                        validity = "Valid"

                    result_document = {
                        "reg_no": register_no,
                        "result_name": resultName,
                        "token": token,
                        "sem": student_result.get("semesterName"),
                        "publishDate": published_date,
                        "result": student_result["resultDetails"],
                        "validity": validity
                    }

                    # Save the result to MongoDB
                    mongo.ezyrec.results.insert_one(result_document)
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching individual student result: {e}")
                    continue

        except requests.exceptions.RequestException as e:
            print(f"Error fetching published results: {e}")
    # Retrieve all valid results for all students with the specified token
    all_student_results = mongo.ezyrec.results.find({"validity": "Valid"})
    serialized_results = []
    for sr in all_student_results:
        student = mongo.ezyrec.student.find_one({"reg_no":sr["reg_no"]})
        serialized_result = {
            "name":student["name"],
            "reg_no": sr["reg_no"],
            "result_name": sr["result_name"],
            "token": sr["token"],
            "sem": sr["sem"],
            "publishDate": sr["publishDate"],
            "result": sr["result"]
        }
        serialized_results.append(serialized_result)

    return jsonify(serialized_results), 200


@app.route('/published-results-student', methods=['POST'])
def published_results_student():
    data = request.json
    register_no = data.get('reg_no')
    student = mongo.ezyrec.student.find_one({"reg_no":register_no})
    date_st = student['dob']
    date_st = datetime.datetime.strptime(str(date_st), "%Y-%m-%d %H:%M:%S")
    date_of_birth = str(date_st.strftime("%Y-%m-%d"))

    join_date_str = student.get('join_date')
    if join_date_str:
        join_date = datetime.datetime.strptime(str(join_date_str), "%Y-%m-%d %H:%M:%S")
    else:
        return jsonify({"error": "Join date not found for the student"}), 404

    join_date_plus_4_months = join_date + relativedelta(months=+4)

    try:
        response = requests.post(OFFICIAL_API_RESULTS_URL, json=PUBLISHED_RESULTS_PAYLOAD, headers=HEADERS, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        published_results = response.json()
        # print(published_results[0])
        for result in published_results:
            if "b.tech" in result['resultName'].lower() or "btech" in result['resultName'].lower() :

                published_date_str = result['publishDate']
                published_date = datetime.datetime.strptime(published_date_str, "%Y-%m-%d")
                
                if published_date <= join_date_plus_4_months:
                    continue  # Skip if published date is not greater than join date + 4 months

                token = result['token']

                # Check if the result for this student already exists in MongoDB
                existing_result = mongo.ezyrec.results.find_one({"reg_no": register_no, "result_name": result['resultName']})
                if existing_result:
                    continue  # Skip if already exists

                # Fetch individual student result
                payload = {
                    "dateOfBirth": date_of_birth,
                    "registerNo": register_no,
                    "token": token
                }
                try:
                    student_response = requests.post(OFFICIAL_API_INDIVIDUAL_RESULT_URL, json=payload, headers=HEADERS, verify=False)
                    student_response.raise_for_status()
                    student_result = student_response.json()

                    if student_result['resultDetails'] == None :
                        validity = "Invalid"
                    else:
                        validity = "Valid"
                    
                    result_document = {
                        "reg_no": register_no,
                        "result_name": result["resultName"],
                        "token": token,
                        "sem": student_result["semesterName"],
                        "publishDate": result['publishDate'],
                        "result": student_result["resultDetails"],
                        "validity": validity
                    }

                    # Save the result to MongoDB
                    mongo.ezyrec.results.insert_one(result_document)
                except requests.exceptions.RequestException as e:
                    continue
        
        student_results = mongo.ezyrec.results.find({"validity":"Valid","reg_no":register_no})

        serialised_results=[]
        for sr in student_results:
            serialised_result={
                "reg_no":sr["reg_no"],
                "result_name":sr["result_name"],
                "token":sr["token"],
                "sem":sr["sem"],
                "publishDate":sr["publishDate"],
                "result":sr["result"]
            }
            serialised_results.append(serialised_result)
        return jsonify(serialised_results), 200
    except requests.exceptions.RequestException as e:
        print(f"Error fetching published results: {e}")
        return jsonify({"error": "Failed to fetch published results"}), 500
    
@app.route('/published-results-allstudents', methods=['POST'])
def published_results_allstudents():
    data = request.json
    token = data.get('token')
    published_date_str = data.get('date')
    resultName = data.get('resultName')

    if not token:
        return jsonify({"error": "Token is required"}), 400

    published_date = datetime.datetime.strptime(published_date_str, "%Y-%m-%d")

    try:
        students = mongo.ezyrec.student.find()

        for student in students:

            join_date_str = student.get('join_date')
            if join_date_str:
                join_date = datetime.datetime.strptime(str(join_date_str), "%Y-%m-%d %H:%M:%S")
            else:
                continue  # Skip if no join_date

            join_date_plus_4_months = join_date + relativedelta(months=+4)
            if published_date <= join_date_plus_4_months:
                continue  # Skip if published date is not greater than join date + 4 months

            register_no = student.get('reg_no')
            date_st = student['dob']
            date_st = datetime.datetime.strptime(str(date_st), "%Y-%m-%d %H:%M:%S")
            date_of_birth = str(date_st.strftime("%Y-%m-%d"))

            # Check if the result for this student and token already exists in MongoDB
            existing_result = mongo.ezyrec.results.find_one({"reg_no": register_no, "result_name": resultName})
            if existing_result:
                continue  # Skip if already exists

            # Fetch individual student result
            payload = {
                "dateOfBirth": date_of_birth,
                "registerNo": register_no,
                "token": token
            }
            try:
                student_response = requests.post(OFFICIAL_API_INDIVIDUAL_RESULT_URL, json=payload, headers=HEADERS, verify=False)
                student_response.raise_for_status()
                student_result = student_response.json()

                if student_result['resultDetails'] is None:
                    validity = "Invalid"
                else:
                    validity = "Valid"

                result_document = {
                    "reg_no": register_no,
                    "result_name": resultName,
                    "token": token,
                    "sem": student_result.get("semesterName"),
                    "publishDate": published_date,
                    "result": student_result["resultDetails"],
                    "validity": validity
                }

                # Save the result to MongoDB
                mongo.ezyrec.results.insert_one(result_document)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching individual student result: {e}")
                continue

        # Retrieve all valid results for all students with the specified token
        all_student_results = mongo.ezyrec.results.find({"validity": "Valid", "result_name": resultName})

        serialized_results = []
        for sr in all_student_results:
            student = mongo.ezyrec.student.find_one({"reg_no":sr["reg_no"]})
            serialized_result = {
                "name":student["name"],
                "reg_no": sr["reg_no"],
                "result_name": sr["result_name"],
                "token": sr["token"],
                "sem": sr["sem"],
                "publishDate": sr["publishDate"],
                "result": sr["result"]
            }
            serialized_results.append(serialized_result)

        return jsonify(serialized_results), 200

    except requests.exceptions.RequestException as e:
        print(f"Error fetching published results: {e}")
        return jsonify({"error": "Failed to fetch published results"}), 500


def delete_expired_otps():
    current_time = datetime.datetime.now(timezone.utc)
    try:
        result = mongo.ezyrec.otp.delete_many({"expires_at": {"$lt": current_time}})
        # print(f"Deleted {result.deleted_count} expired OTPs")
    except Exception as e:
        print(f"Error deleting expired OTPs: {e}")

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_otps, trigger="interval", seconds=60)
scheduler.start()
 
if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        scheduler.shutdown()
