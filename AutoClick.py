import time
import pyautogui
refreshPos = [100,400]
#print(pyautogui.position())

while 1:
    time.sleep(5)
    pyautogui.click(button = 'right', x = refreshPos[0], y = refreshPos[1])
    time.sleep(1)
    pyautogui.click(button = 'left', x = refreshPos[0] + 20, y = refreshPos[1] + 120)

    time.sleep(3)
    #pyautogui.click(button = 'right', x = 100, y = 400)
    pyautogui.click(button = 'left', x = 100, y = 400)
    pyautogui.scroll(-10000, x = 100, y = 400)
    time.sleep(1)
    """
    pyautogui.click(button = 'right', x = 120, y = 510)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 130, y = 520)
    time.sleep(2)
    
    pyautogui.click(button = 'left', x = 1052, y = 52)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 1052, y = 165)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 1123, y = 263)
    time.sleep(1)
    """
    pyautogui.click(button = 'right', x = 120, y = 510)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 130, y = 520)
    time.sleep(5)

    pyautogui.click(button = 'right', x = 120, y = 490)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 130, y = 500)
    time.sleep(5)

    """
    pyautogui.click(button = 'left', x = 1052, y = 52)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 1052, y = 165)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 1123, y = 263)
    time.sleep(1)
    
    pyautogui.click(button = 'right', x = 120, y = 490)
    time.sleep(1)
    pyautogui.click(button = 'left', x = 130, y = 500)
    time.sleep(1)
    """
    time.sleep(180)

"""
while 1:
    time.sleep(1)
    print(pyautogui.position())
#pyautogui.click(button = 'right', x = 100, y = 450)
"""