# RC Results Parser, by Ian Renton

import csv
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

# Get command-line variables
main_url = sys.argv[1]
output_path = sys.argv[2]

# Load main page
print("Loading " + main_url + "...")
main_page = urllib.request.urlopen(main_url)
main_page_soup = BeautifulSoup(main_page, 'html.parser')

# Set up data storage
races = []

# Find and extract all Race Result page URLs
for result_link in main_page_soup.find_all('a'):
    if "RaceResult" in result_link.get('href'):
        result_page_url = urllib.parse.urljoin(main_url, result_link.get('href'))

        # Load the Race Result page
        result_page = urllib.request.urlopen(result_page_url)
        result_page_soup = BeautifulSoup(result_page, 'html.parser')

        # Get a title for the race
        race_title = " - ".join(str(heading.text) for heading in result_page_soup.find_all('h3'))
        print("Processing " + race_title)
        race_data = {"race_title": race_title, "race_data": []}

        # Get driver results pages
        for driver_result_link in result_page_soup.find_all('a'):
            if "DriverResult" in driver_result_link.get('href'):
                driver_result_page_url = urllib.parse.urljoin(main_url, driver_result_link.get('href'))

                # Load contents
                driver_result_page = urllib.request.urlopen(driver_result_page_url)
                driver_result_page_soup = BeautifulSoup(driver_result_page, 'html.parser')
                tables = driver_result_page_soup.find_all('table')

                # Get driver name
                driver_name = tables[0].find_all('td')[1].text

                # Get lap times
                lap_time_fields = tables[1].find_all('td', {'class': 'text-right'})
                lap_times = [x.text for x in lap_time_fields]

                # Store data
                driver_result = {"driver_name": driver_name, "lap_times": lap_times}
                race_data["race_data"].append(driver_result)

        # Store data
        races.append(race_data)

# Start writing data to file
print("Writing to " + output_path + "...")
output_file = open(output_path, "w", newline="")
writer = csv.writer(output_file)

for race in races:
    # Write race title on the first line, then lines starting with driver name, followed by all lap times
    writer.writerow([race["race_title"]])
    for driver_result in race["race_data"]:
        writer.writerow([driver_result["driver_name"]] + driver_result["lap_times"])
    # End with a gap before the next race
    writer.writerow([])

output_file.close()
print("Done!")
