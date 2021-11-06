import json
import requests
import sys

def drive_upload(filepath, file_name):
    
    try:
        headers = {"Authorization": "Bearer ya29.a0ARrdaM_4vRpD6p9KQCg5thefWk6kbeqeXJaB1E5skGczhiE7-Z9UJutIRzvd6U9gG4jsYNOtOq73ezXye2m0LGWNjKHHKveWhJ39HTHwR-mjfZEN282NVsZBME25XpSXhKAcS5g4d9fEbS7zgA1HX0VwTWhJ"}
        para = {
            "name": file_name,
            "parents":["1Y9hs9auNLbnqh7Y0QmXorVevmUq-3XFI"]
        }
        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open("./"+filepath, "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        print(r.text)
        
        # Clear folder contents (Make modular depending on what extension is specified
        # p = subprocess.Popen([sys.executable, 'clear_folder.py', '.h264', 'Videos'], stdout=subprocess.PIPE)
        # p = subprocess.Popen([sys.executable, 'clear_folder.py', '.jpg', 'Images'], stdout=subprocess.PIPE)
        
    except Exception as e:
      print("The file was not sent")
    finally:
        print('Closing the drive connection')

drive_upload(sys.argv[1], sys.argv[2])



