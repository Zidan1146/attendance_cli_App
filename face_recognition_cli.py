import os
import face_recognition
import json
import shutil
from attendance_constants import *


def create_subfolder(main_folder, is_file_mode):
    subfolder_path = os.path.join(DATA_FOLDER, main_folder)

    if not os.path.exists(subfolder_path) and is_file_mode:
        os.mkdir(subfolder_path)

    return subfolder_path

def copy_and_rename_file(image_file, subfolder_path, main_folder, index):
    try:
        file_ext = os.path.splitext(image_file)[1]

        if file_ext.lower() not in ['.jpg', '.jpeg', '.png']:
            return

        shutil.copy(image_file, subfolder_path)

        new_file_name = f'{main_folder}_{index:02d}{file_ext}'
        new_file_path = os.path.join(subfolder_path, new_file_name)
        os.rename(os.path.join(subfolder_path, os.path.basename(image_file)), new_file_path)

    except FileNotFoundError:
        print(f'Could not copy {image_file} to {subfolder_path} because it does not exist.')

def copy_folder(main_folder, subfolder_path):
    shutil.copytree(main_folder, subfolder_path)

    for i, file_name in enumerate(os.listdir(subfolder_path)):
        old_file_path = os.path.join(subfolder_path, file_name)

        if not file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            os.remove(old_file_path)
            continue

        file_ext = os.path.splitext(file_name)[1]
        new_file_name = f'{main_folder}_{i + 1:02d}{file_ext}'
        new_file_path = os.path.join(subfolder_path, new_file_name)
        os.rename(old_file_path, new_file_path)

def sort_subfolders(subfolder_path):
    # Get a list of folders in the directory
    folders = os.listdir(DATA_FOLDER)

    folder_to_remove = []
    
    try:
        for folder in folders:
            prefix, sep, suffix = folder.partition("_")
            if prefix.isdigit():
                os.rename(os.path.join(DATA_FOLDER, folder), os.path.join(DATA_FOLDER, suffix))
                folder_to_remove.append(folder)
                folders.append(suffix)
    except OSError:
        shutil.rmtree(os.path.join(DATA_FOLDER,folder.split("_")[1]))
        os.rename(os.path.join(DATA_FOLDER, folder), os.path.join(DATA_FOLDER, suffix))
        folder_to_remove.append(folder)
        print(f'Cannot copy directory, directory exists: {subfolder_path}')
        input()
    
    for item in folder_to_remove:
        folders.remove(item)
    
    # Sort the folder names in ascending order
    sorted_folders = sorted(folders)

    for i, subfolder_name in enumerate(sorted_folders):
        old_subfolder_path = os.path.join(DATA_FOLDER, subfolder_name)
        prefix, sep, suffix = subfolder_name.partition('_')
        new_subfolder_name = f'{i + 1:02d}_{subfolder_name}'
        new_subfolder_path = os.path.join(DATA_FOLDER, new_subfolder_name)
        os.rename(old_subfolder_path, new_subfolder_path)

def add_file_data(main_folder, *image_files):
    subfolder_path = create_subfolder(main_folder, True)

    for i, image_file in enumerate(image_files):
        copy_and_rename_file(image_file, subfolder_path, main_folder, i)

    sort_subfolders(main_folder)
    
    if SETTINGS['load_after_add']:
        load_data()

def add_folder_data(*folders):
    for folder in folders:
        subfolder_path = create_subfolder(folder, False)
        try:
            copy_folder(folder, subfolder_path)
        except Exception as e:
            print(f"Error copying folder '{folder}': {e}")
            return

        sort_subfolders(folder)
    
    if SETTINGS['load_after_add']:
        load_data()


def load_dataset_from_json():
    dataset = []

    # Create the JSON folder if it doesn't exist
    if not os.path.exists(JSON_FOLDER):
        os.mkdir(JSON_FOLDER)

    # Load the JSON data if it exists and has 'encoding' attribute
    if os.path.isfile(KNOWN_FACE_PATH):
        with open(KNOWN_FACE_PATH, 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0 and 'encoding' in data[0]:
                dataset = data

    return dataset


def load_images(dataset):
    total_image = sum(len(files) for root, dirs, files in os.walk(DATA_FOLDER))
    image_processed = 0
    
    for root, dirs, files in os.walk(DATA_FOLDER):
        for file in files:
            image_processed = image_processed + 1
            print(f'Loading image {file}... ({image_processed}/{total_image})')
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                # Check if image with the same path already exists in the dataset
                if any(image['image_path'] == image_path for image in dataset):
                    print(f'{file} already exists in the dataset. Skipping...')
                    continue
                try:
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)[0]
                    name = os.path.basename(os.path.dirname(image_path).split("_")[1])
                    id = int(os.path.basename(os.path.dirname(image_path).split("_")[0]))
                    dataset.append({
                        'id': id,
                        'image_path': image_path,
                        'name': name,
                        'encoding': encoding.tolist()
                    })
                except (IndexError, ValueError):
                    # If the face encoding cannot be computed, remove the invalid image
                    print(f'Could not compute encoding for {file}. Removing image...')
                    os.remove(image_path)
                    continue
            else:
                # If the file is not an image, remove it
                invalid_file_path = os.path.join(root, file)
                os.remove(invalid_file_path)

    # Sort the dataset by ID
    dataset = sorted(dataset, key=lambda x: int(x['id']))

    return dataset


def save_dataset_to_json(dataset):
    # Save the dataset to JSON
    with open(KNOWN_FACE_PATH, 'w') as f:
        json.dump(dataset, f, indent=4)

    print('All images loaded!')


def load_data():
    dataset = load_dataset_from_json()
    dataset = load_images(dataset)
    save_dataset_to_json(dataset)


def configuration(config, value):
    settings = SETTINGS
    
    if os.path.exists(SETTINGS_JSON_PATH):
        with open(SETTINGS_JSON_PATH, 'r') as f:
            settings = json.load(f)
    elif not os.path.exists(JSON_FOLDER):
        os.mkdir(JSON_FOLDER)
    
    if config == 'time_in':
        hours = value // 3600
        minutes = (value % 3600) // 60
        seconds = value % 60
        
        settings[f'{config}_hours'] = hours
        settings[f'{config}_minutes'] = minutes
        settings[f'{config}_seconds'] = seconds
    else:
        settings[config] = value
    
    with open(SETTINGS_JSON_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    
    print(f'Configured {config}')