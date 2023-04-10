from datetime import datetime, time
import os
import json

# Settings
SETTINGS_JSON_PATH = 'storage/json/settings.json'
if os.path.exists(SETTINGS_JSON_PATH):
    with open(SETTINGS_JSON_PATH) as f:
        SETTINGS = json.load(f)
else:
    SETTINGS = {
        'time_in_hours' : 8,
        'time_in_minutes' : 0,
        'time_in_seconds' : 0,
        'capture_mode' : False,
        'load_after_add' : False
    }

# Paths and Filenames
STORAGE_FOLDER = 'storage'
JSON_FOLDER = f'{STORAGE_FOLDER}/json'
KNOWN_FACE_PATH = f'{JSON_FOLDER}/known_faces.json'

DATABASE_FOLDER = f'{STORAGE_FOLDER}/database'
ATTENDANCE_DB = f'{DATABASE_FOLDER}/attendance.db'
CURRENT_DATE = f'attendance_at_{datetime.now().strftime("%Y_%m_%d")}'

DATA_FOLDER = f'{STORAGE_FOLDER}/Faces_Data'
SAVED_IMAGE_FOLDER = f'{STORAGE_FOLDER}/captured_images'

# Database Queries
TOLERANCE = 0.5
ENTER_TIME = time(SETTINGS['time_in_hours'], SETTINGS['time_in_minutes'], SETTINGS['time_in_seconds']).strftime('%H:%M:%S')
ADD_TO_DATABASE = f'INSERT INTO {CURRENT_DATE} (no_absence, name, time, status) SELECT ?, ?, ?, ?'
DELETE_COPY = f'''DELETE FROM {CURRENT_DATE}
WHERE id NOT IN (
    SELECT MIN(id) FROM {CURRENT_DATE}
    GROUP BY name
);'''
EXTRACT_TIME = f'SELECT time FROM {CURRENT_DATE} WHERE name = ?'

# Create some folders if they don't exist
if not os.path.exists(STORAGE_FOLDER):
    os.mkdir(STORAGE_FOLDER)

if not os.path.exists(SAVED_IMAGE_FOLDER):
    os.mkdir(SAVED_IMAGE_FOLDER)

if not os.path.exists(JSON_FOLDER):
    os.mkdir(JSON_FOLDER)

if not os.path.exists(DATABASE_FOLDER):
    os.mkdir(DATABASE_FOLDER)
