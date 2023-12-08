# RC Results Parser

Converts results from rc-results.com into a CSV file for later processing.

Written by Ian Renton, December 2023

## Setting up your environment

1. Ensure you have python version >= 3.8 installed
2. Clone the repository from Github, and open the directory in a terminal window
3. Optionally, create a virtual environment ("venv") to install libraries separately to your system Python libraries, with e.g. `venv ./venv`
4. Install the required dependencies by running `pip install -r requirements.txt`

## Running

Run with two arguments:

1. URL of meeting summary page
2. Output CSV file

e.g. `rc-results-parser.py http://www.rc-results.com/viewer/Main/MeetingSummary?meetingId=10075 output.csv`