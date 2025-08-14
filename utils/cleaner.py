import os

def clean_temp(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)