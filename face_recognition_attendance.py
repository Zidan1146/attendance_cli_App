import cv2
import numpy as np
import sqlite3
from datetime import datetime, time
import os
import face_recognition
import json
from attendance_constants import KNOWN_FACE_PATH as KNOWN_FACES_FILE
from attendance_constants import *

def check_is_late(current_time):
    if current_time <= ENTER_TIME:
        return 'On Time'
    else:
        return 'Late'


def create_database(cursor):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {CURRENT_DATE} (id INTEGER PRIMARY KEY, no_absence INTEGER, name TEXT, time TEXT, status TEXT)")


def load_known_faces():
    with open(KNOWN_FACES_FILE, 'r') as f:
        dataset = json.load(f)
        
    known_faces_encodings = [np.array(data['encoding'], dtype=float) for data in dataset]
    known_names = [data['name'] for data in dataset]
    known_id = [data['id'] for data in dataset]
    return known_faces_encodings, known_names, known_id


def process_frame(frame, known_faces_encodings, known_names, known_id, id_times_dict, cursor, conn):
    frame = cv2.flip(frame, 1)
    now = datetime.now()
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=TOLERANCE)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
            id = known_id[best_match_index]

            if name not in id_times_dict:
                current_time = now.strftime("%H:%M:%S")
                id_times_dict[name] = current_time
                status = check_is_late(current_time)
                val = (id, name, current_time, status)
                cursor.execute(ADD_TO_DATABASE, val)
                cursor.execute(DELETE_COPY)
                conn.commit()
                if SETTINGS['capture_mode']:
                    cv2.imwrite(f'{SAVED_IMAGE_FOLDER}/{name}_at_{datetime.now().strftime("%Y_%m_%d")}.jpg', frame)

        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        timed = f'- {id_times_dict[name]}' if name in id_times_dict else ''
        cv2.putText(frame, f'{name} {timed}', (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame


def load_id_times_dict(cursor, known_names):
    id_times_dict = {}
    for name in known_names:
        cursor.execute(EXTRACT_TIME, (name, ))
        value = cursor.fetchone()
        if value != None:
            id_times_dict[name] = value[0]
    return id_times_dict


def main():    
    conn = sqlite3.connect(ATTENDANCE_DB)
    cursor = conn.cursor()

    create_database(cursor)
    known_faces_encodings, known_names, known_id = load_known_faces()
    id_times_dict = load_id_times_dict(cursor, known_names)
    
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print('Error reading frame from camera')
            break

        frame = process_frame(frame, known_faces_encodings, known_names, known_id, id_times_dict, cursor, conn)
        cv2.imshow('Press "Esc" to exit', frame)

        if cv2.waitKey(1) == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
