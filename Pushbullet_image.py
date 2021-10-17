import sys
from pushbullet import Pushbullet

API_KEY = "XXXXXXXXXXXXXXXXXXXX"

pb = Pushbullet(API_KEY)

def file_upload(filename):
    try:
        with open(filename, "rb") as picture:
            file_data = pb.upload_file(picture, filename)

        push = pb.push_file(**file_data)
    except Exception as e:
      print("The file was not sent")
    finally:
        print('Closing the Pushbullet API connection')
         
    
file_upload(sys.argv[1])
