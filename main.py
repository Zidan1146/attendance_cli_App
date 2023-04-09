import argparse
import os

from face_recognition_attendance import main as start_attendance
from face_recognition_cli import add_file_data, add_folder_data,load_data, configuration
from database_view import main as view_attendance


def start_mode(args):
    """Starts the attendance process."""
    start_attendance()


def add_mode(args):
    """Adds new face data."""
    if args.input_type == 'file':
        add_file_data(args.folder_name, *args.files)
    elif args.input_type == 'folder':
        args.input_data.append(args.data_folder)
        add_folder_data(*args.input_data)


def settings_mode(args):
    """Set the configuration"""
    # TODO: add function to configure settings
    if args.config != 'time_in':
        args.value = bool(args.value)
    
    configuration(args.config, args.value)


def load_mode(args):
    """Loads existing face data for attendance tracking."""
    load_data()


def view_mode(args):
    """Shows attendance data."""
    view_attendance()


def main():
    """Parse command line arguments and call the appropriate function."""
    parser = argparse.ArgumentParser(description='Attendance tracking with face recognition.')
    subparsers = parser.add_subparsers(dest='mode', help='Available commands')

    start_parser = subparsers.add_parser('start', help='Start the attendance process.')
    start_parser.set_defaults(func=start_mode)

    add_parser = subparsers.add_parser('add', help='Add new face data to the program.')
    add_parser.add_argument('input_type', help='Specify whether the input is a single file or a folder containing multiple files.', choices=['file', 'folder'])
    add_parser.add_argument('data_folder', help='Name of the folder containing face images.')
    add_parser.add_argument('input_data', nargs='*', help='List of file or folder names of face images to add.')
    add_parser.set_defaults(func=add_mode)

    settings_parser = subparsers.add_parser('set', help='Set a configuration parameter.')
    settings_parser.add_argument('config', help='Configuration type', choices=['time_in', 'capture_mode', 'load_after_add'])
    settings_parser.add_argument('value', help='Configuration value', type=int)
    settings_parser.set_defaults(func=settings_mode)

    subparsers.add_parser('load', help='Load existing face data for attendance tracking.').set_defaults(func=load_mode)
    subparsers.add_parser('view', help='Show attendance data.').set_defaults(func=view_mode)    

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
