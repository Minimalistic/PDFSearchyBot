# PDFSearchyBot

## Description
A simple script that can be customized for use - Assign a URL for a PDF to be downloaded and scanned for certain keywords.  Typically the usage is that the PDF is changing occasionally and you're wanting to be alerted to any pertinent updates to its contents.

## Setup
Make a duplicate of the `config.py.example` file and rename it to `config.py`.
Populate the search and URL list.  Currently this program uses a lower security
gmail account configuration. I have a dedicated gmail account just for this to
ensure my security and privacy aren't affected. 

For more information on how to customize your gmail account to be compatible
with this program, have a look [here](https://towardsdatascience.com/send-data-alert-with-python-smtp-efb9ee08077e)