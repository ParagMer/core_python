import os
import shutil
import hashlib
import re
from datetime import datetime

def get_image_hash(image_path):
    """Generate a hash for the image file to detect duplicates."""
    hash_sha1 = hashlib.sha1()
    with open(image_path, 'rb') as file:
        while chunk := file.read(8192):  # Read file in chunks
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

def move_images_by_extension(source_dir, target_dir):
    """Move images based on file extension."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path) and re.match(r'.*\.(jpg|jpeg|png|gif|bmp)', filename, re.IGNORECASE):
            target_path = os.path.join(target_dir, filename)
            print(f"Moving {filename} to {target_path}")
            shutil.move(file_path, target_path)

def move_images_by_date(source_dir, target_dir):
    """Move images into folders based on creation date."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path) and re.match(r'.*\.(jpg|jpeg|png|gif|bmp)', filename, re.IGNORECASE):
            creation_date = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')
            date_folder = os.path.join(target_dir, creation_date)

            if not os.path.exists(date_folder):
                os.makedirs(date_folder)

            target_path = os.path.join(date_folder, filename)
            print(f"Moving {filename} to {target_path}")
            shutil.move(file_path, target_path)

def delete_duplicate_images(directory):
    """Delete duplicate images based on file hash."""
    hashes = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and re.match(r'.*\.(jpg|jpeg|png|gif|bmp)', filename, re.IGNORECASE):
            file_hash = get_image_hash(file_path)

            if file_hash in hashes:
                print(f"Duplicate found: {filename}")
                os.remove(file_path)  # Delete the duplicate image
            else:
                hashes[file_hash] = file_path

def main():
    source_dir = input("Enter the source directory for images: ")
    target_dir = input("Enter the target directory to move images: ")

    # Move images by extension
    move_images_by_extension(source_dir, target_dir)

    # Alternatively, move images by date (uncomment below to use)
    # move_images_by_date(source_dir, target_dir)

    # Delete duplicate images (if any)
    delete_duplicate_images(target_dir)
    print("Organizing complete!")

if __name__ == "__main__":
    main()
