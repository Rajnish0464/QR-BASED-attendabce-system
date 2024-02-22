import qrcode
import cv2
import mysql.connector as connector
from datetime import date
import pyttsx3
import pandas as pd

# Read the CSV file
file = pd.read_csv('attendance_sheet.csv')

# Define a dictionary to store attendance status
attendance = {}

class DBhelper:
    def __init__(self):
        self.con = connector.connect(
            host="localhost",
            user="root",
            password="rajnish",
            database="student_data"
        )

        query = 'create table if not exists student(StudentId int primary key, StudentName varchar(200), enroll_No varchar(20))'

        cur = self.con.cursor()
        cur.execute(query)
        print("Created")

    # Insert user into the database
    def insert_user(self, StudentId, StudentName, enroll_No):
        query = "insert into student(StudentId, StudentName, enroll_No) values({},'{}','{}')".format(StudentId, StudentName, enroll_No)
        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("User saved to db")

    def fetch_all(self):
        students = []
        query = "select * from student"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            print(row)
            students.append(row[1])
        return students

    def add_date_col(self, date):
        # Add a new column for each date to store attendance
        query = 'ALTER TABLE student ADD COLUMN `{}` varchar(20)'.format(date)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def add_att(self, date, student_name, stat):
        # Update attendance for a specific date
        query = "UPDATE student SET `{}` = '{}' WHERE StudentName = '{}'".format(date, stat, student_name)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

# Initialize the database helper
helper = DBhelper()

# Fetch all existing students from the database
students = helper.fetch_all()

# Generate QR code for each student
for student in students:
    # Create a unique code for each student
    qr_code = qrcode.make(student)
    # Save the QR code as an image file
    qr_code.save(f"{student}.png")

# Initialize camera
cap = cv2.VideoCapture(0)

# Capture video until 'q' key is pressed
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('frame', frame)

    # Decode QR code
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(frame)

    # Mark student as present
    if data in students:
        attendance[data] = True

        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set the speech rate (optional)
        engine.setProperty('rate', 150)  # You can adjust the value as needed

        # Set the speech volume (optional)
        engine.setProperty('volume', 1.0)  # You can adjust the value between 0 and 1

        # Specify the text to be spoken
        text = data + " present"

        # Speak the text
        engine.say(text)
        engine.runAndWait()

    # Quit program when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()

today = date.today()
date_str = today.strftime("%d/%m/%Y")

# Add a new column for today's date
helper.add_date_col(date_str)

# Print attendance report
print("====================================")
print("      Attendance Report:")
print("====================================")

for student, present in attendance.items():
    status = "Present" if present else "Absent"
    print(f"{student}: {status}")
    helper.add_att(date_str, student, status)

print("====================================")
file.to_csv('attendance_sheet.csv', index=False)
wait = input("Press Enter to exit")
print("Press q to exit")
