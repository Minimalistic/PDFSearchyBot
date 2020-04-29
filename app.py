#!/usr/bin/python3

# Used for `definitions.py` to define a variable to Project Root
import os
# Used for exiting application
import sys
# for downloading file from URL
import urllib.request
from PyPDF2 import PdfFileReader
import PyPDF2

# for emailing alerts
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Config file to be filled with search word, other sensitive info
from config import searchWord, \
    urlList,				   \
    email_sender_account,	   \
    email_sender_username,	   \
    email_sender_password,	   \
    email_smtp_server,		   \
    email_smtp_port,		   \
    email_recipients

# Give the downloaded file a name
downloadedFile = ''

# Used for storing a single detected match
searchMatch = ''

# A list for collecting all detected matches
detectedMatches = []

search_word_count = 0

print('PDFSearchyBot is now beginning file download...')

# Iterate over the urlList
for item in urlList:

    # Store downloaded filename for later
    downloadedFile = os.path.basename(item)
    # Note, urllib docs state urlretrieve will possibly be deprecated...someday.
    # Download file(item) from url in urlList
    urllib.request.urlretrieve(item, downloadedFile)

    # Open downloaded file, extract all text and run a search
    with open(downloadedFile, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f, strict=False)
        for page in reader.pages:
            extractedText = page.extractText()
            if (extractedText.find(searchWord) >= 0):
                print("Possible match for " + searchWord)
                searchMatch = True
        if searchMatch == False:
            print("No matches for "
                  + searchWord + " in " + downloadedFile)

    # Email Section

    # Store the found matches so email body can indicate where they are.
    detectedMatches.append(downloadedFile)
    # Login to email service
    server = smtplib.SMTP(email_smtp_server, email_smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_sender_username, email_sender_password)

    # For loop, sending emails to all recipients listed in config.py
    for recipient in email_recipients:
        print(f"Sending email to {recipient}")
        message = MIMEMultipart('alternative')
        message['From'] = email_sender_account
        message['To'] = recipient
        message['Subject'] = "PDFSearchyBot has detected matches"

        # This looks rather clunky
        email_body = f"""
            *Alert* PDFSearchyBot has detected a match
            in the following files:
            <br>
            <br>
            """ + "<br>".join(str(match) for match in detectedMatches)
        message['Content-Type'] = 'text/html'
        message.attach(MIMEText(email_body, 'html'))
        text = message.as_string()
        server.sendmail(email_sender_account, recipient, text)

# All emails sent, log out.
server.quit()
print("All emails have been sent, logged out.")

# file cleanup of downloaded files
for file in detectedMatches:
    os.remove(file)
    print(file + " deleted.")

print("Program complete, now exiting.")
sys.exit()
