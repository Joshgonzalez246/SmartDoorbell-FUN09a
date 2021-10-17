import os, sys, time

path = '/home/pi/Doorbell/'

def clear_contents(folder, file_ext):
    
    try:
        for x in os.listdir(folder):
            if x.endswith(file_ext):
                print('Deleting file:', x)
                os.unlink(folder + '/' + x)
                time.sleep(2)
                print('File deleted')
                
        print('All files in ' + folder + ": have been deleted successfully")
    except Exception as e:
        print('An error occurred')
     
# define the file extension and the folder to be cleared of all its data
folder = sys.argv[2]
target = sys.argv[1]
clear_contents(folder, target)