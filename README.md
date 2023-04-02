# Documentation for Attendance System

## Introduction
This Attendance System is built using face recognition technology. It can recognize the faces of registered individuals and mark their attendance automatically. It can also store and view attendance data. This system is built in Python language using OpenCV, dlib, and face_recognition libraries.

## Prerequisites
- OpenCV
- dlib
- face_recognition
- numpy

## Installation
1. Install Python 3.x on your computer.

2. Install the required libraries using pip. For example, to install OpenCV, you can run the following command in your terminal:
```bash
pip install opencv_contrib_python
```
## Usage
To use this system, you need to run the main.py file in your terminal using the following command:
```bash
python main.py [mode] [folder name] [file names...]
```
Where:

- [mode] is the mode of operation. It can be one of the following:

  - start: starts the attendance process.
  - add: adds a new folder with the specified name to the image data directory and adds the provided files to that folder.
  - load: loads existing face data for attendance tracking.
  - view: shows attendance data.
  - help: displays a list of available commands.

- [folder name] is the name of the folder to add face data. It is only required if the mode is add.

- [file names...] are the names of the image files to add to the folder. They are only required if the mode is add.

## Examples
- To start the attendance process, run the following command:
```bash
python main.py start
```

- To add a new folder named "students" with two image files named "image1.jpg" and "image2.jpg", run the following command:
```bash
python main.py add students image1.jpg image2.jpg
```

- To add an entire folder named "teachers" to the image data directory, run the following command:
```bash
python main.py add teachers
```

- To load existing face data, run the following command:
```bash
python main.py load
```

- To view attendance data, run the following command:
```bash
python main.py view
```

- To display a list of available commands, run the following command:
```bash
python main.py help
```

## Notes
- The face_recognition_attendance module is used for attendance tracking.
- The face_recognition_cli module is used for adding or loading face data.
- The database_view module is used for viewing attendance data.
- The images are stored in the "Faces" directory. Each - subfolder corresponds to a registered individual.
- The face data is stored in the "known_faces.json" file in the "json" directory. It is used for face recognition during attendance tracking.
- The attendance data is stored in the "attendance.db" file in the "Database" directory. It contains the date, time, and name of each registered individual who attended the event.

