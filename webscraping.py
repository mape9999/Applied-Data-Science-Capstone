
'''
Objective: Web scrape Falcon 9 launch records  from Wikipedia

'''

# Import libraries
import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings) if data_time.strip()][:2]

def booster_version(table_cells):
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0 and booster_version.strip()][:1])
    return out

def landing_status(table_cells):
    out = [i for i in table_cells.strings if i.strip()][0]
    return out

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass and "kg" in mass:
        new_mass = mass[:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    column_name = ' '.join([content.strip() for content in row.contents if content.strip()]) 
    column_name = column_name.strip() 
    
    if not column_name.isdigit(): 
        return column_name    

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
response = requests.get(static_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    print("Page Title: ", soup.title.string) #Page Title:  List of Falcon 9 and Falcon Heavy launches - Wikipedia
    
    html_tables = soup.find_all("table")
    print("Number of tables found: {}".format(len(html_tables))) # 26
else:
    print("Failed to retrieve data: {}".format(response.status_code))

# Check the content for the 3rd table
first_launch_table = html_tables[2]
print(first_launch_table)

# Extract relevant column names from the HTML table headers by iterating through <th> elements

# Apply find_all() function with `th` element on first_launch_table
header_cells = first_launch_table.find_all("th")

# Extract column names and filter out empty names
column_names = []
for header in header_cells:
    name = extract_column_from_header(header)
    if name is not None and len(name) > 0:
        column_names.append(name)
print("Column Names: {}".format(column_names))
# Column Names: ['Flight No.', 'Date and time ( )', 'Launch site', 'Payload', 'Payload mass', 'Orbit', 'Customer', 'Launch outcome']

# Turn the HTML tables into a data frame

# Initialize an empty dictionary with keys for all the column names
launch_dict= dict.fromkeys(column_names) # initially each key is set to None

# Remove one column - Dat and time, from launch_dict
del launch_dict['Date and time ( )']

# Re-initialize the exisitng keys )columns) so they point to empty lists. Will be filles, row-by-row when extracting data.
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []

# Add new columns (keys) to the dictionary
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

# Remove unexpected annotations, missing values and correct inconsistent formatting.
extracted_row = 0

# Extract each table
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # get table row
    for rows in table.find_all("tr"):
        # check to see if first table heading is a number corresponding to a launch number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False

        # get table element
        row = rows.find_all('td')

        # if it is a number, save cells in a dictionary
        if flag:
            extracted_row += 1

            # Flight Number: Append the flight_number into launch_dict with key `Flight No.`
            launch_dict["Flight No."].append(flight_number)

            # Extract date/time from the first column
            datatimelist = date_time(row[0])

            # Date: Append the date into launch_dict with key `Date`
            date = datatimelist[0].strip(',')
            launch_dict["Date"].append(date)

            # Time: Append the time into launch_dict with key `Time`
            time = datatimelist[1]
            launch_dict["Time"].append(time)

            # Booster version: Append the bv into launch_dict with key `Version Booster`
            bv = booster_version(row[1])
            if not bv:  # if booster_version() returned None or empty
                bv = row[1].a.string
            print(bv)
            launch_dict["Version Booster"].append(bv)

            # Launch Site: Append the launch_site into launch_dict with key `Launch site`
            launch_site = row[2].a.string
            #print(launch_site)
            launch_dict["Launch site"].append(launch_site)

            # Payload: Append the payload into launch_dict with key `Payload`
            payload = row[3].a.string
            #print(payload)
            launch_dict["Payload"].append(payload)

            # Payload Mass: Append the payload_mass into launch_dict with key `Payload mass`
            payload_mass = get_mass(row[4])
            #print(payload_mass)
            launch_dict["Payload mass"].append(payload_mass)

            # Append the orbit into launch_dict with key `Orbit`
            orbit = row[5].a.string
            #print(orbit)
            launch_dict["Orbit"].append(orbit)

            # Append customer with key Customer
            if row[6].a is not None:
                customer = row[6].a.string
            else:
                customer = None
            launch_dict["Customer"].append(customer)

            # Append the launch_outcome into launch_dict with key `Launch outcome`
            launch_outcome = list(row[7].strings)[0]
            #print(launch_outcome)
            launch_dict["Launch outcome"].append(launch_outcome)

            # Booster landing
            booster_landing = landing_status(row[8])
            #print(booster_landing)
            launch_dict["Booster landing"].append(booster_landing)

# Create a data frame from the dictionary
df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })

# Save to CSV
#df.to_csv('spacex_web_scraped.csv', index= False)

# Export to HTML
df.to_html('table2.html', index=False)