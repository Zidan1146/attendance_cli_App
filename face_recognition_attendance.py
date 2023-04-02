import cv2
import numpy as np
import sqlite3
from datetime import datetime, time
import os
import face_recognition
import json

def check_is_late(current_time):
    # Define the time that an student is expected to enter the workplace (8:00 AM)
    enterHours = time(8,0,0).strftime('%H:%M:%S')
    if current_time <= enterHours:
        # If the student arrived on time or earlier than expected, return "On Time"
        return 'On Time'
    elif current_time > enterHours:
        # If the student arrived later than expected, return "Late"
        return 'Late'

def create_database(current_date, c):
    # Create a table for the current date if it doesn't exist
    c.execute(f"CREATE TABLE IF NOT EXISTS {current_date} (id INTEGER PRIMARY KEY, no_absence INTEGER, name TEXT, time TEXT, status TEXT)")

def load_known_faces():
    # Load the known faces' encodings, names, and IDs from the JSON file
    known_faces_encodings = []
    known_names = []
    known_id = []
    
    with open('json/known_faces.json', 'r') as f:
        dataset = json.load(f)
    
    for data in dataset:
        # Convert the encoding from a list to a numpy array of floats
        encodings = np.array(data['encoding'], dtype=float)
        known_id.append(data['id'])
        known_names.append(data['name'])
        known_faces_encodings.append(encodings)
    
    return known_faces_encodings, known_names, known_id

def main():
    # Check if "database" folder exists, create it if it does not exist
    if not os.path.exists('database'):
        os.mkdir('database')
        
    # Connect to SQLite database file
    conn = sqlite3.connect('database/attendance.db')
    c = conn.cursor()
    
    # Create a new table for the current date if it does not exist
    now = datetime.now()
    current_date = f'attendance_at_{now.strftime("%Y_%m_%d")}'
    create_database(current_date, c)
    
    # Load known faces encodings and corresponding names and ids from JSON file
    known_faces_encodings, known_names, known_id =  load_known_faces()
    
    # Initialize a dictionary to store the time when each person was recognized
    id_times_dict = {}

    # Open the webcam for video capture
    capture = cv2.VideoCapture(0)
    
    # Start the main loop
    while True:
        # Get the current time
        now = datetime.now()
        
        # Read a frame from the video capture
        is_true, frame = capture.read()
        
        # Flip the frame horizontally for intuitive display
        frame = cv2.flip(frame, 1)

        # Locate faces in the current frame and encode them
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Iterate over each face encoding and location
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare the current face encoding to known faces encodings
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.5)
            
            # Initialize name as "Unknown"
            name = "Unknown"

            # Calculate the distances between the current face encoding and known faces encodings
            face_distances = face_recognition.face_distance(known_faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            # If the best match index is a match
            if matches[best_match_index]:
                # Get the name and id of the recognized person
                name = known_names[best_match_index]
                id = known_id[best_match_index]
                
                # If the person has not been recognized before in the current session
                if name not in id_times_dict:
                    # Get the current time and check if the person is late
                    current_time = now.strftime("%H:%M:%S")
                    id_times_dict[name] = current_time
                    status = check_is_late(current_time)

                    # Insert attendance record into database
                    sql = f'''INSERT INTO {current_date} (no_absence, name, time, status) 
                    SELECT ?, ?, ?, ?'''
                    
                    val = (id, name, current_time, status)
                    c.execute(sql, val)
                    
                    # Delete duplicate attendance records and commit the transaction
                    delete_sql = f'''DELETE FROM {current_date}
                                    WHERE id NOT IN (
                                        SELECT MIN(id) FROM {current_date}
                                        GROUP BY name
                                    );'''

                    c.execute(delete_sql)
                    conn.commit()

            # Draw a bounding box around the recognized face and label it with the name and time if available
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            timed = f'- {id_times_dict[name]}' if name in id_times_dict else ''
            cv2.putText(frame, f'{name} {timed}', (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Press "Esc" button to exit', frame)

        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
