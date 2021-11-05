import pyautogui
import time
MeetingID = 'fcu-uqkz-ntx'
InitiateMeet = (205, 715)
JoinNow = (1350, 650)
StartInstantMeeting = (280, 770)
time.sleep(0.5)

# meetingID = pyautogui.prompt(text='Enter your meeting ID', title='Meeting ID', default='')
# time.sleep(0.5)

#Command to search and open Google Chrome
pyautogui.press('win', interval=0.5)
time.sleep(0.5)
pyautogui.typewrite('chrome', interval=0.2)
time.sleep(0.5)
pyautogui.press('enter', interval=0.5)
time.sleep(3)

#Type Google meet URL
pyautogui.typewrite('https://meet.google.com/', interval=0.1)
time.sleep(0.5)
pyautogui.press('enter', interval=0.5)
time.sleep(5)

# Initiate meeting on website
pyautogui.click(InitiateMeet)
time.sleep(0.5)
pyautogui.click(StartInstantMeeting)
time.sleep(7.5)
#Enter the location of the meeting code box
# pyautogui.typewrite(MeetingID, interval=0.2)
# time.sleep(0.5)
# pyautogui.press('enter', interval=0.2)
# time.sleep(7.5)

#Enter the location of the 'Join Now' button
# pyautogui.click(JoinNow)
# time.sleep(5)
