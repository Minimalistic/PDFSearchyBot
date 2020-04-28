#!/usr/bin/python3


import os # Used for `definitions.py` to define a variable to Project Root
import urllib.request
from PyPDF2 import PdfFileReader
import PyPDF2

# for emailing alerts
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Config file to be filled with search word, other sensitive info
from config import searchWord,				\
				   fileURL,					\
				   email_sender_account,	\
				   email_sender_username,	\
				   email_sender_password,	\
				   email_smtp_server,		\
				   email_smtp_port,			\
				   email_recipients,		\
				   email_subject,			\
				   email_body

# variable to be changed to True if a match has been found.
searchMatch = False

# Give the downloaded file a name
downloadedFile = 'DownloadedFile.pdf'

search_word_count = 0

print('PDF Grab N Scan is now beginning file download to specified folder...')

with open(downloadedFile, mode='rb') as f:
	reader = PyPDF2.PdfFileReader(f, strict=False)
	for page in reader.pages:
		extractedText = page.extractText()
		if (extractedText.find(searchWord) != -1):
			print ("Defined word has likely been found in the downloaded PDF.")
			searchMatch = True
			print(searchWord)
			
#### Email Section

#login to email server

server = smtplib.SMTP(email_smtp_server, email_smtp_port)
server.ehlo()
server.starttls()
server.login(email_sender_username, email_sender_password)

#For loop, sending emails to all recipients
for recipient in email_recipients:
	print(f"Sending email to {recipient}")
	message = MIMEMultipart('alternative')
	message['From'] = email_sender_account
	message['To'] = recipient
	message['Subject'] = email_subject
	message.attach(MIMEText(email_body, 'html'))
	text = message.as_string()
	server.sendmail(email_sender_account, recipient, text)

#All emails sent, log out.
server.quit()


# TODO file cleanup after process completed