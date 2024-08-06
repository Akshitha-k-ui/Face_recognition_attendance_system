from flask import Flask, render_template, session,request, redirect, url_for ,flash,Response, jsonify
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# contact
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login/signupdb'

mysql = MySQL(app)
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone=request.form['phone']
        message = request.form['message']
    

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contact (name, email, phone, message) VALUES (%s, %s, %s,%s)', (name, email, phone,message))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Message sent successfully'})
        return redirect('/')


# face camera on
@app.route('/start')
def start():
    return render_template('index1.html')


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    with open('attendance.csv', 'a') as f:
        f.write(f'\n{name},{dt_string}')
    return now

path = 'imageAttendance'
images = []
classnames = []
myList = os.listdir(path)
for cl in myList:
    currentimg = cv2.imread(f'{path}/{cl}')
    images.append(currentimg)
    classnames.append(os.path.splitext(cl)[0])



encodelistKnown = findEncodings(images)
print('Encoding complete')

camera = cv2.VideoCapture(0)

recognized_name = ""
last_marked_times = {}

def gen_frames():
    global recognized_name
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

            facecurframe = face_recognition.face_locations(imgs)
            encodecurframe = face_recognition.face_encodings(imgs, facecurframe)

            for encodeface, faceloc in zip(encodecurframe, facecurframe):
                matches = face_recognition.compare_faces(encodelistKnown, encodeface)
                facedis = face_recognition.face_distance(encodelistKnown, encodeface)
                matchindex = np.argmin(facedis)

                if matches[matchindex]:
                    name = classnames[matchindex].upper()
                    recognized_name = name  # Update the recognized name
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y1 - 35), (x2, y1), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/index1.html')
def index1():
    return render_template('index1.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    global recognized_name, last_marked_times
    now = datetime.now()

     # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify(status='fail', message='Please login to continue. <a href="#" id="login-link">Login</a>')


    if recognized_name:
        if recognized_name in last_marked_times:
            time_diff = now - last_marked_times[recognized_name]
            if time_diff.total_seconds() < 30:
                return jsonify(status='fail', message='Attendance already marked recently')
        
        last_marked_times[recognized_name] = markAttendance(recognized_name)
        return jsonify(status='success', name=recognized_name)
    else:
        return jsonify(status='fail', message='No face recognized')
    

# login/signup db
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['newUsername']
        email = request.form['email']
        password = request.form['newPassword']

        # Check if username or email already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        user = cursor.fetchone()
        if user:
             return jsonify({'success': False, 'message': 'Username or email already exists!'}), 400

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cursor.close()
        session['logged_in'] = True


        return jsonify({'success': True, 'message': 'Signup successful!'}), 200

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        session['logged_in'] = True

        if user:
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password!'}), 400
        

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # Clear the session when the user logs out
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
