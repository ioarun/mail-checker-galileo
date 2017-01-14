#!/usr/bin/env python

from imapclient import IMAPClient
import time
import sys

DEBUG = True

HOSTNAME = 'imap-mail.outlook.com'  #imap.gmail.com for gmail accounts
USERNAME = 'your username here'
PASSWORD = 'your password here'
MAILBOX = 'Inbox'

NEWMAIL_OFFSET = 0   # minimum number of unread messages
MAIL_CHECK_FREQ = 60 # check mail every 60 seconds

def pins_export():
    try:
        pin1export = open("/sys/class/gpio/export","w")
        pin1export.write("38")
        pin1export.close()
    except IOError:
        print "INFO: GPIO 7 already exists, skipping export"

    fp1 = open( "/sys/class/gpio/gpio38/direction", "w" )
    fp1.write( "out" )
    fp1.close()

def write_led( value ):
    fp2 = open( "/sys/class/gpio/gpio38/value", "w" )
    fp2.write( str( value ) )
    fp2.close()


pins_export()


def loop():
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)

    if DEBUG:
        print('Logging in as ' + USERNAME)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info['EXISTS'])

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])

    if DEBUG:
        print "You have", newmails, "new emails!"

    if newmails > NEWMAIL_OFFSET:
        write_led(1)
    else:
	write_led(0)

    time.sleep(MAIL_CHECK_FREQ)

if __name__ == '__main__':
	while True :
		loop()
