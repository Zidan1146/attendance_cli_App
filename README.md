# Documentation for Attendance System

## Introduction
This Attendance System is built using face recognition technology. It can recognize the faces of registered individuals and mark their attendance automatically. It can also store and view attendance data. This system is built in Python language using OpenCV, dlib, and face_recognition libraries.

## Prerequisites
- Python 3.x
- OpenCV
- dlib
- face_recognition

## Installation
1. Install Python 3.x on your computer.

2. Install the required libraries using pip. For example, to install OpenCV, you can run the following command in your terminal:
```bash
pip install opencv_contrib_python
pip install dlib
pip install face-recognition
```
## Usage
To use this system, you need to run the **main.py** file in your terminal using the following command:
```bash
python main.py [command] [arguments]
```
Where:

- **command** is the command to execute. It can be one of the following:

  - **start**: starts the attendance process.
  - **add**: adds new face data to the program.
  - **set**: sets a configuration parameter.
  - **load**: loads existing face data for attendance tracking.
  - **view**: shows attendance data.

- **arguments** are the arguments for the command.


### **start** command
To start the attendance process, run the following command:
```bash
python main.py start
```

### **add** command
To add new face data, use the add command. There are two ways to add face data:

#### Add files
To add a multiple files, run the following command:
```bash
python main.py add file [folder_name] [file_path...]
```
Where:

- **folder_name** is the name of the folder to add the face data to.
- **file_path** is the path to the image file.

#### Add a folder of files
To add a folder of files, run the following command:
```bash
python main.py add folder [folder_path...]
```
Where:
- **folder_path** is the path to the folder containing the image files.

### **set** command
To set a configuration parameter, use the set command. The following configuration parameters are available:

- **time_in**: Set the class start time deadline for students in the format of a 24-hour clock (e.g. 8:00 for 8 AM). The default value is 8:00 AM.
- **capture_mode**: Set the face capture mode to determine whether or not the system should capture an image of the person's face after recognition. If set to true, the system will capture an image. If set to false, the system will not capture anything. The default value is False
- **load_after_add**: Set whether or not to load the new face data automatically after it is added. The default value is False.
To set a configuration parameter, run the following command:

```bash
python main.py set [parameter] [value]
```
Where:

- **parameter** is the name of the parameter to set.
- **value** is the value to set the parameter to.

### **load** command
To load existing face data, run the following command:
```bash
python main.py load
```
### **view** command
To view attendance data, run the following command:
```bash
python main.py view
```

## Notes
- The **storage** folder is the top-level directory where all data related to the attendance system is stored.
- The **json** folder inside the **storage** folder contains JSON files that store configuration settings and face recognition data.
- The **known_faces.json** file in the **json** folder stores the face encoding data for all registered students.
- The **database** folder inside the **storage** folder contains an SQLite database file that stores attendance data.
- The **attendance.db** file in the **database** folder is the SQLite database file used to store attendance data.
- The **Faces_Data** folder inside the **storage** folder is where the system looks for new face data to be added to the system.
- The **captured_images** folder inside the **storage** folder is where the system stores captured images when **capture_mode** is set to **True**.
