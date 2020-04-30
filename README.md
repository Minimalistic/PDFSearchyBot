# PDFSearchyBot

## Description
*Note - Currently, this only works with PDF files and static URLs*

A simple script that can be customized for use - Add a list of URLs for scanning, scipt then downloads each file found at those URLs and scans for specified keyword. Finally, it emails the detected keyword matches along with links to the pertinent files.

## Setup

Make a duplicate of the `config.py.example` file and rename it to `config.py`. Populate the search and URL list.  Currently this program uses a lower security gmail account configuration. I recommend a dedicated gmail account for sending the emails.

For more information on how to customize your gmail account to be compatible with this program, have a look [here](https://towardsdatascience.com/send-data-alert-with-python-smtp-efb9ee08077e)