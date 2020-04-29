#!/usr/bin/python3

# Used for `definitions.py` to define a variable to Project Root
import os
# for downloading file from URL
import urllib.request
from PyPDF2 import PdfFileReader
import PyPDF2

# for emailing alerts
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Config file to be filled with search word, other sensitive info
from config import searchWord,				\
				   urlList,				    \
				   email_sender_account,	\
				   email_sender_username,	\
				   email_sender_password,	\
				   email_smtp_server,		\
				   email_smtp_port,			\
				   email_recipients

# Variable is changed to True if a match has been found.
searchMatch = False

# Give the downloaded file a name
downloadedFile = ''

detectedMatches = []

search_word_count = 0

print('PDFSearchyBot is now beginning file download...')


# Iterate over the urlList
for item in urlList:

	downloadedFile = os.path.basename(item)
	# Note, urllib docs state urlretrieve will possibly be deprecated...someday.
	urllib.request.urlretrieve(item, downloadedFile)
	
	with open(downloadedFile, mode='rb') as f:
		reader = PyPDF2.PdfFileReader(f, strict=False)
		for page in reader.pages:
			extractedText = page.extractText()
			if (extractedText.find(searchWord) >= 0):
				print ("Possible match for " + searchWord)
				searchMatch = True
		if searchMatch == False:
			print("No matches for " \
				+ searchWord + " in " + downloadedFile)

	#### Email Section

	# Login to email server

	# Store the found matches so email body can indicate where they are.
	detectedMatches.append(downloadedFile)
	server = smtplib.SMTP(email_smtp_server, email_smtp_port)
	server.ehlo()
	server.starttls()
	server.login(email_sender_username, email_sender_password)

	# For loop, sending emails to all recipients
	for recipient in email_recipients:
		print(f"Sending email to {recipient}")
		message = MIMEMultipart('alternative')
		message['From'] = email_sender_account
		message['To'] = recipient
		message['Subject'] = "PDFSearchyBot found matches"

		# This looks rather horrific
		email_body = f"""
This is an automated message on behalf of Jason Marsh from PDFSearchyBot.<br>
<br>
Every 12 hours, PDFSearchyBot downloads the St.Louis County Jail Roster and it \
runs a search within the downloaded PDF file, if it finds a match, \
it then sends out this email alert to addresses that Jason has pre-selected.\
<br>
<br>
*Alert* PDFSearchyBot has detected a match! <br><br>
Here are the links to the PDF files where there were matches: <br>
<br>
""" + "<br>".join(str(match) for match in detectedMatches)
		message['Content-Type'] = 'text/html'
		message.attach(MIMEText(email_body, 'html'))
		text = message.as_string()
		server.sendmail(email_sender_account, recipient, text)

	#All emails sent, log out.
	server.quit()

# TODO add file cleanup after file searched.