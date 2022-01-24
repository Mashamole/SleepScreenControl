import random
import pyautogui
import time
from datetime import datetime
"""
PyautoGui Functions

(1)
print(pyautogui.position())  # prints mouse position on screen

(2)
# move mouse to XY coordinates over num_second seconds
# pyautogui.moveTo(x1, y1)
# pyautogui.moveTo(x2, y2, duration=2)

(3)
print(pyautogui.size())  # prints resolution of screen

(4)
# Able to choose mouse [button] to click (left/right/middle)
pyautogui.click(x=x1, y=y1, clicks=1, button='left') 

(5)
print(pyautogui.onScreen(x, y)) # True if x & y are within the screen.

(6)
pyautogui.PAUSE = 2.5 #can set delays between each pyautogui call
"""
x1 = 3799
y1 = 470
x2 = 3799
y2 = 922


# i = 0
# while True:
#     if(i == 10):
#         break
#     # print(pyautogui.position())
#     pyautogui.moveTo(x1, y1)
#     pyautogui.moveTo(x2, y2, duration=2)
#     time.sleep(.8)
#    i += 1

# BottomRight (x=3308, y=1370)
# topLeft (x=2762, y=524)
# TopMid (x=3055, y=426)b
# middleLeft (x=2612, y=902)
# BottomMid Point(x=2993, y=1891)
# BottomBottomRight(x=3462, y=2022)
# LeftMid(x=1466, y=872)
# TopLeft(x=1290, y=478)
# BottomLeft(x=323, y=1877)
pyautogui.FAILSAFE = False
dtNow = datetime.now()  # use for Time-Elapsed info [Time Elapsed] -

print(f"\nTimeStamp (START) -> {dtNow.strftime('%H:%M:%S')}")
# seconds = dtNow.strftime('%S')
# print(seconds)
j = 0
while True:  # Add random clicks to right side of screen
    # seconds = dtNow.strftime('%S')
    timeCheck = datetime.now()
    if j == 30:
        # Clicks only able to prevent screen to sleep
        pyautogui.leftClick(x=random.randint(2766, 3462),
                            y=random.randint(370, 2022))
        print(f"TimeStamp (Check) -> {timeCheck.strftime('%H:%M:%S')}")
        j = 0
    # print(j)
    time.sleep(1)
    j += 1
# pyautogui.click(x=x1, y=y1, clicks=1, button='left')

# move mouse to XY coordinates over num_second seconds
# pyautogui.moveTo(x1, y1)
# pyautogui.moveTo(x2, y2, duration=2)
# pyautogui.leftClick()
