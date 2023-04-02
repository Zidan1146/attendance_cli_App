import os
import face_recognition
import json
import shutil

def add_data(main_folder, *image_files):
    # Set the path to the main folder
    data_path = 'Faces'

    # Create the subfolder if there are image files
    if len(image_files) > 0:
        subfolder_path = os.path.join(data_path, main_folder)
        os.mkdir(subfolder_path)

        # Copy and rename each image file
        for i, image_file in enumerate(image_files):
            try:
                file_ext = os.path.splitext(image_file)[1]
                shutil.copy(image_file, subfolder_path)
            except FileNotFoundError:
                os.rmdir(subfolder_path)
                print(f'Could not copy {image_file} to {subfolder_path} because it does not exist.')
                print(f'{subfolder_path} deleted')
                input()
                return
            os.rename(image_file, f'{subfolder_path}_{i:02d}{file_ext}')

    # If there are no image files, copy the entire folder
    elif len(image_files) == 0:
        subfolder_path = os.path.join(data_path, main_folder)
        shutil.copytree(main_folder, subfolder_path)
        files = os.listdir(os.path.join(data_path, main_folder))
        
        for index, file in enumerate(files):
            file_ext = os.path.splitext(file)[1]
            old_file_path = os.path.join(subfolder_path, file)
            new_file_name = f'{main_folder}_{index + 1:02d}{file_ext}'
            new_file_path = os.path.join(subfolder_path, new_file_name)
            os.rename(old_file_path, new_file_path)


    # Get a list of folders in the directory
    folders = os.listdir(data_path)

    folder_to_remove = []
    
    try:
        for folder in folders:
            prefix, sep, suffix = folder.partition("_")
            if prefix.isdigit():
                os.rename(os.path.join(data_path, folder), os.path.join(data_path, suffix))
                folder_to_remove.append(folder)
                folders.append(suffix)
    except OSError:
        shutil.rmtree(subfolder_path)
        print(f'Cannot copy directory, directory exists: {subfolder_path}')
        input()
        return
    
    for item in folder_to_remove:
        folders.remove(item)
        
    # Sort the folder names in ascending order
    sorted_folders = sorted(folders)

    # Rename each folder in ascending order
    for i, folder_name in enumerate(sorted_folders):
        # Split the folder name into prefix and suffix
        prefix, sep, suffix = folder_name.partition("_")

        # Check if the prefix is a number
        if prefix.isdigit():
            folder = folder_name.split('_')[1]
            # Increment the prefix and format it with leading zeros
            new_prefix = f"{i + 1:02d}_{folder}"
        else:
            # If the prefix is not a number, use 01 as the new prefix
            new_prefix = f"{i + 1:02d}_{folder_name}"

        # Create the new folder name by concatenating the new prefix and the suffix
        new_folder_name = new_prefix

        # Get the full path of the folder to rename
        folder_to_rename = os.path.join(data_path, folder_name)

        # Get the full path of the new folder name
        new_folder_path = os.path.join(data_path, new_folder_name)

        # Rename the folder
        os.rename(folder_to_rename, new_folder_path)

    load_data()

def load_data():
    known_faces_folder = 'Faces'
    dataset = []
    known_faces_file = 'json/known_faces.json'
    folder = known_faces_file.split('/')[0]
    
    if os.path.isfile(known_faces_file) and 'encoding' in known_faces_file:
        with open(known_faces_file, 'r') as f:
            dataset = json.load(f)
    elif not os.path.exists(folder):
        os.mkdir(folder)
    
    for root, dirs, files in os.walk(known_faces_folder):
        for i, file in enumerate(files):
            print(f'Loading image {file}... ({i + 1}/{len(files)})')
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                image_path = os.path.join(root, file)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                name = os.path.dirname(image_path.split('_')[1]).split(os.sep)[-1]
                id = int(os.path.dirname(image_path).split(os.sep)[-1].split('_')[0])
                dataset.append({
                    'id': id,
                    'image_path': image_path,
                    'name': name,
                    'encoding': encoding.tolist()
                })
    
    with open(known_faces_file, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print('All image Loaded!')
    input()
