import face_recognition_attendance  # importing a module for attendance tracking
import face_recognition_cli  # importing a module for face recognition
import database_view  # importing a module for viewing attendance data
import os  # importing a module for interacting with the operating system
import sys  # importing a module for accessing system-specific parameters and functions

def main():
    files = []  # creating an empty list to hold file names
    
    # checking the number of command line arguments
    if len(sys.argv) == 2:
        mode = str(sys.argv[1])  # if there's one argument, it's the mode
    elif len(sys.argv) == 3:
        mode = str(sys.argv[1])  # if there are two arguments, the first is the mode, and the second is the folder name
        if mode == 'add':  # if the mode is "add"
            folder_name = str(sys.argv[2])  # the third argument is the folder name
    elif len(sys.argv) > 3:
        mode = str(sys.argv[1])  # if there are more than two arguments, the first is the mode, the second is the folder name, and the rest are files
        if mode == 'add':  # if the mode is "add"
            folder_name = str(sys.argv[2])  # the third argument is the folder name
            for i in range(3, len(sys.argv)):
                files.append(sys.argv[i])  # the rest of the arguments are file names, so add them to the list
    else:
        mode = 'help'  # if there are no arguments or an invalid number, default to "help"
        
    mode = mode.lower()  # convert the mode to lowercase
    
    # check the mode and call the appropriate function
    if mode == 'start':
        face_recognition_attendance.main()  # call the function to start attendance tracking
    elif mode == 'add':
        face_recognition_cli.add_data(folder_name, *files)  # call the function to add new face data
    elif mode == 'load':
        face_recognition_cli.load_data()  # call the function to load existing face data
    elif mode == 'view':
        database_view.main()  # call the function to view attendance data
    elif mode == 'help':
        # if the mode is "help", print a list of available commands
        print('Available commands')
        print('"start" : starts the attendance process.')
        print('"add [folder name] [file names...]" : adds a new folder with the specified name to the image data directory and adds the provided files to that folder.')
        print('"add [folder name] : add the copy of the provided folder to the image data directory')
        print('"load" : loads existing face data for attendance tracking.')
        print('"view" : shows attendance data.')
        print('"help" : displays a list of available commands.')

if __name__ == '__main__':
    main()  # call the main function if the script is run directly
