# Objective: Load the Spacex_dataset into a table in the Db2 database
# Includes a record for each payload carried during a SpaceX mission
# Execute queries to understand the dataset better

import sqlite3
import pandas as pd

# Load the data from CSV
df = pd.read_csv('Spacex.csv')

# Print columns to debug
print("Columns in DataFrame:", df.columns)

# Convert Date column to ISO format (YYYY-MM-DD)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Rename columns to avoid spaces in SQL
df.columns = df.columns.str.replace(' ', '_')  # Replaces spaces with underscores

# Use a context manager for the database connection
with sqlite3.connect("spacex.db") as conn:
    cur = conn.cursor()

    # Drop the table if it already exists
    cur.execute("DROP TABLE IF EXISTS spacex")

    # Load the DataFrame into the SQLite table
    df.to_sql('spacex', conn, if_exists='replace', index=False, method='multi')

    # Query to display unique launch sites
    cur.execute('SELECT DISTINCT Launch_site FROM spacex')
    unique_launch_sites = cur.fetchall()
    print("Unique Launch Sites:")
    for site in unique_launch_sites:
        print(site[0])

    # Display 5 records where launch sites begin with 'CCA'
    cur.execute("SELECT * FROM spacex WHERE Launch_site LIKE 'CCA%' LIMIT 5")
    records = cur.fetchall()
    print("\nRecords where Launch sites begin with 'CCA':")
    for record in records:
        print(record)

    # Calculate total payload mass by NASA
    cur.execute("""
        SELECT SUM(CAST("PAYLOAD_MASS__KG_" AS FLOAT)) 
        FROM spacex 
        WHERE Customer = 'NASA (CRS)'
    """)
    total_payload_mass = cur.fetchone()[0]
    print("Total Payload Mass carried by NASA (CRS): {} kg".format(total_payload_mass if total_payload_mass else 0))

    # Calculate average payload mass for booster version F9 v1.1
    cur.execute("""
        SELECT AVG(CAST("PAYLOAD_MASS__KG_" AS FLOAT)) 
        FROM spacex 
        WHERE "Booster_Version" = 'F9 v1.1'
    """)
    average_payload_mass = cur.fetchone()[0]
    print("Average Payload Mass carried by booster version F9 v1.1: {} kg".format(round(average_payload_mass, 2) if average_payload_mass else 0))

    # Find the date of the first successful landing outcome on a ground pad
    cur.execute("""
        SELECT MIN(Date) 
        FROM spacex 
        WHERE "Landing_Outcome" LIKE '%Success%'
    """)
    first_successful_landing_date = cur.fetchone()[0]
    print("Date of the first successful landing outcome: {}".format(first_successful_landing_date))
    
    # List successful drone ship landings and payload mass btw 4000-6000kg. 
    cur.execute("""
        SELECT DISTINCT Booster_Version 
        FROM spacex 
        WHERE Landing_Outcome LIKE '%Success%'
        AND CAST(PAYLOAD_MASS__KG_ AS FLOAT) BETWEEN 4000 AND 6000
    """)
    successful_boosters = cur.fetchall()

    if successful_boosters:
        print("Boosters with successful drone ship landings and payload mass between 4000 and 6000 kg:")
        for booster in successful_boosters:
            print(booster[0])
    else:
        print("No matching boosters found.")

 #   cur.execute("SELECT DISTINCT Landing_Outcome FROM spacex")
 #   print(cur.fetchall())  #[('Failure (parachute)',), ('No attempt',), ('Uncontrolled (ocean)',), ('Controlled (ocean)',), ('Fai'Success',), ('Failure',), ('No attempt ',)]

 #   cur.execute("SELECT MIN(PAYLOAD_MASS__KG_), MAX(PAYLOAD_MASS__KG_) FROM spacex")
 #   print(cur.fetchall())  #[(0, 15600)]

 #   cur.execute("SELECT DISTINCT Booster_Version FROM spacex")
 #   print(cur.fetchall())  
       
          
    # Count number of successful and failure mission outcomes
    # The Landing_Outcome column contains inconsistent data. Clean the data.
    cur.execute("""
        UPDATE spacex
        SET "Landing_Outcome" = TRIM("Landing_Outcome");
      """)
    cur.execute("""
        UPDATE spacex
        SET "Landing_Outcome" = 'Success'
        WHERE "Landing_Outcome" LIKE '%Success%';
    """)
    cur.execute("""
        UPDATE spacex
        SET "Landing_Outcome" = 'Failure'
        WHERE "Landing_Outcome" LIKE '%Failure%';
    """)
    
    cur.execute("""
        SELECT LOWER(TRIM("Landing_Outcome")) AS landing, COUNT(*) AS total
        FROM spacex
        WHERE LOWER(TRIM("Landing_Outcome")) IN ('success', 'failure')
        GROUP BY LOWER(TRIM("Landing_Outcome"))
    """)
    outcomes = cur.fetchall()
    
    successful_count = 0
    failed_count = 0
    
    for outcome in outcomes:
        if outcome[0] == 'success':
            successful_count += outcome[1]
        elif outcome[0] == 'failure':
            failed_count += outcome[1]
    print("Successful outcome: {} and Failed outcome: {}".format(successful_count, failed_count))
    
    # List the names of the booster versions which have carried max payload mass.
    cur.execute("""
        SELECT DISTINCT "Booster_Version"
        FROM spacex
        WHERE CAST("PAYLOAD_MASS__KG_" AS FLOAT) = (
            SELECT MAX(CAST("PAYLOAD_MASS__KG_" AS FLOAT))
            FROM spacex
        )
    """)
    booster_versions = cur.fetchall()
    print("Booster versions that have carried the maximum payload mass:")
    for version in booster_versions:
        print(version[0])
    
    
    # List the records which display the month, failure landing_outcomes, booster version, launch_site in year 2015

 #   cur.execute("PRAGMA table_info(spacex);")
 #   columns = cur.fetchall()
 #   print(columns)

    cur.execute("""
    SELECT "Launch_Site", "Booster_Version", "Landing_Outcome", "Date"
    FROM spacex
    WHERE TRIM("Landing_Outcome") = 'Failure'
    AND strftime('%Y', "Date") = '2015';
""")
    failure_records_2015 = cur.fetchall()

    print("Records with failure landing outcomes in 2015:")
    if failure_records_2015:
        for record in failure_records_2015:
            print(record)
    else:
        print("No failure landing outcomes found for the year 2015.")

    # Rank the count of landing outcomes between 2010-06-04 and 2017-03-20
    cur.execute("""
        SELECT
            TRIM(UPPER("Landing_Outcome")) AS LandingOutcome,
            COUNT(*) AS LandingCount
        FROM spacex
        WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
        GROUP BY Landing_Outcome
        ORDER BY LandingCount DESC;
    """)

    landing_outcomes = cur.fetchall()
    print("\nLanding Outcomes Ranking:")
    for outcome in landing_outcomes:
        print(f"{outcome[0]}: {outcome[1]}")

print("Data loaded and queries executed successfully.")
