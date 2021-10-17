import json
import requests
import sys

def drive_upload(filepath, file_name):
    
    try:
        headers = {"Authorization": "Bearer ya29.a0ARrdaM9pYAPteDN4bBUAl_ehwlT8xqgqZNRYGQH-j-uVyt7MEjz2geGTlvqc2w9M1wR08YWJ5S8xvwwiZI6BjS2rYuNU1ZR53nUoDqTYVP9mCXxksqQjvWY6hnW26RqQyAszD15EVNWqNLfXdERRBabSMPmX"}
        para = {
            "name": file_name,
            "parents":["13u3OP3k35nU7m-bhiH4NBu5UftifxmfM"]
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
        p = subprocess.Popen([sys.executable, 'clear_folder.py', '.h264', 'Videos'], stdout=subprocess.PIPE)
        p = subprocess.Popen([sys.executable, 'clear_folder.py', '.jpg', 'Images'], stdout=subprocess.PIPE)
        
    except Exception as e:
      print("The file was not sent")
    finally:
        print('Closing the drive connection')

drive_upload(sys.argv[1], sys.argv[2])



