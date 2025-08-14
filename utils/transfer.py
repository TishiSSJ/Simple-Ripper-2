import requests

def upload(file_path):
    with open(file_path, 'rb') as f:
        response = requests.put(
            'https://transfer.sh/' + file_path.split("/")[-1], data=f)
    return response.text.strip()