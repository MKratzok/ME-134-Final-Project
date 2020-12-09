"""
Max Kratzok
12-5-2020

Steps:
    1) Rename and save this file to /home/pi/send_img.py

    2) Make a new email address

    3) Set Gmail Permissions allow less secure apps (https://myaccount.google.com/lesssecureapps)

    4) Fill in the fields marked below

    5) Check send_img.py

        pi ~$ python3 send_ip_img.py

    5) On your Pi, set up the automatic service:

        pi ~$ sudo systemctl edit --force --full send_img.service

    6) Paste the contents of the attached file "send_img.service" into that file

    7) Check the new service:

        pi ~$ systemctl status send_img.service
        ● send_img.service - Send IP Address Service
            Loaded: loaded (/etc/systemd/system/send_img.service; disabled; vendor preset: enabled)
            Active: inactive (dead)


    8) Enable and test the service:

        pi ~$ sudo systemctl enable send_img.service
        pi ~$ sudo systemctl start send_img.service
        pi ~$ sudo systemctl start send_img.service

        If you do not receive an email, check previous steps.

    9) Reboot and make sure it works!

        pi ~$ sudo systemctl reboot

    10) If it does not work, check if the network service is disabled and enable it

        pi ~$ systemctl is-enabled systemd-networkd-wait-online.service
        disabled

        pi ~$ sudo systemctl enable systemd-networkd-wait-online.service


Sources:
    https://bc-robotics.com/tutorials/sending-email-using-python-raspberry-pi/#:~:text=%20Sending%20An%20Email%20Using%20Python%20On%20The,Gmail%20and%20create%20a%20new%20email...%20More%20
    https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established
    https://www.freedesktop.org/wiki/Software/systemd/NetworkTarget/
    https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python#:~:text=In%20this%20article%2C%20we%20will%20see%20how%20we,It%20creates%20SMTP%20client%20session%20objects%20for%20mailing.
"""

import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from time import sleep

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
KEY = '&5UX0!tuY3C8HIWo$sT@dE#LxOfy%lRj1eKb)P(^gkcMr7SA2DwZavQB4*nmNhz6FJGpVq9i'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'MaxKsRaspberryPi@gmail.com'
GMAIL_PASSWORD = 'kak6rravQ'
SENDTO = 'kratzok@gmail.com'
PHOTO_PATH = "/home/pi/SecurityPhoto.jpg"


def get_ip():
    """
    get_ip() - Gets IP Address
    :return: str - Raspberry Pi's IP Address
    """
    resp = str(subprocess.check_output(["ifconfig", "wlan0"]))
    resp = resp[resp.find("inet") + 5: resp.find("netmask")-2]
    return resp


def get_network():
    """
    get_network() - Gets Wifi Network Name
    :return: str - SSID for the Wifi Network the Raspberry Pi connected to
    """
    ssid = str(subprocess.check_output(["iwgetid"]))
    ssid = ssid[ssid.find("ESSID:") + 6:-3]
    return ssid


def snap_photo(camera):
    """
    snap_photo() - Takes a photo and saves it to PHOTO_PATH
    :return: None
    """
    camera.start_preview()
    sleep(5)
    camera.capture(PHOTO_PATH)
    camera.stop_preview()


def encode(arr, alpha=LETTERS, key=KEY):
    """
    encode
    :param arr: array of strings to be encoded
    :param alpha: alphabet
    :param key: encryption key
    :return: encoded array
    """
    tr = str.maketrans(alpha, key)

    res = []
    for line in arr:
        res.append(line.translate(tr))

    return res


def decode(arr, alpha=LETTERS, key=KEY):
    return encode(arr, key, alpha)


class Emailer:
    def sendmail(self, recipient, subject, content, fname=''):
        """
        sendmail(self, recipient, subject, content, fname) - Sends an email
        :param recipient: str - the recipient's email address
        :param subject: str - the subject of the email
        :param content: str - the message of the email
        :param fname: str - a file's name to be attached to the email [optional]
        :return: None
        """
        # Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        # Login to Gmail
        session.login(GMAIL_USERNAME, ''.join(decode(GMAIL_PASSWORD)))

        # Create Base Message
        message = MIMEMultipart()
        message["From"] = GMAIL_USERNAME
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(content, 'plain'))

        # Add Attachment
        if fname != '':
            attachment = open(fname, 'rb')
            obj = MIMEBase('application', 'octet-stream')
            obj.set_payload(attachment.read())
            encoders.encode_base64(obj)
            obj.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(fname))
            message.attach(obj)

        my_message = message.as_string()

        # Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, my_message)
        session.quit


def run(cam):
    snap_photo(cam)

    sender = Emailer()

    email_subject = "LERMON Photo"
    email_content = "Here is the LERMON Photo."

    sender.sendmail(SENDTO, email_subject, email_content, PHOTO_PATH)


if __name__ == '__main__':
    snap_photo()

    sender = Emailer()

    email_subject = "Your Pi IP is " + get_ip()
    email_content = ("Connected to " + get_network() +
                     "\n\nHere is the security photo.")

    sender.sendmail(SENDTO, email_subject, email_content, PHOTO_PATH)
