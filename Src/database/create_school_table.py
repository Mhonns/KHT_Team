import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config
import pandas as pd

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_school_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        with psycopg2.connect(**params) as connection:
            with connection.cursor() as crsc:
                # create school table
                CREATE_TABLE = """CREATE TABLE IF NOT EXISTS school (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        village_name VARCHAR(256),
                        created_time VARCHAR(256),
                        zoho_secondary_id VARCHAR(256),
                        zoho_primary_id VARCHAR(256),
                        secondary_school_name VARCHAR(256),
                        primary_school_name VARCHAR(256)
                    );"""
                crsc.execute(CREATE_TABLE)

                # Input and output file paths
                input_file_path = get_file_path('Data/Villages_001.csv')
                output_file_path = get_file_path('schools.csv')

                # Select columns and save to a new CSV file
                columns_to_select = ['Village Name', 'Created Time', 'Nearest Mathayom (Seconary) Id', 'Nearest Pratom (Primary) Id']

                select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

                # Fetch the 'created_time' column from the 'villagetest' table
                crsc.execute("SELECT created_time FROM district;")
                existing_times = [item[0] for item in crsc.fetchall()]

                # Load the new CSV data into a DataFrame
                new_data = pd.read_csv(output_file_path)

                # Filter the new data to only include rows with 'created_time' values that don't exist in the database
                new_data = new_data[~new_data['created_time'].isin(existing_times)]

                # If there are no new rows, print a message and return
                if new_data.empty:
                    print('No new rows to add.')
                    return
                else:
                    print('Adding new rows to the district table...')

                # Save the filtered data to a new CSV file
                new_data.to_csv(output_file_path, index=False)

                # Use 'copy_expert' to copy the new data from the CSV file into the 'villagetest' table
                with open(output_file_path, 'r') as f:
                    next(f)  # Skip the header
                    crsc.copy_expert(
                        "COPY school (village_name, created_time, zoho_secondary_id, zoho_primary_id) FROM STDIN WITH CSV HEADER",
                        f
                    )
                connection.commit()

                # based on the zoho_secondary_id and zoho_primary_id relationship with record id in the district table, update the secondary_school_name and primary_school_name columns
                UPDATE_SECONDARY_SCHOOL_NAME = """UPDATE school
                                                SET secondary_school_name = district.town_district_name
                                                FROM district
                                                WHERE school.zoho_secondary_id = district.record_id;"""
                crsc.execute(UPDATE_SECONDARY_SCHOOL_NAME)
                connection.commit()

                UPDATE_PRIMARY_SCHOOL_NAME = """UPDATE school
                                                SET primary_school_name = district.town_district_name
                                                FROM district
                                                WHERE school.zoho_primary_id = district.record_id;"""
                crsc.execute(UPDATE_PRIMARY_SCHOOL_NAME)
                connection.commit()

                # Delete rows with null values in the zoho_secondary_id, zoho_primary_id, secondary_school_name, and primary_school_name columns
                DELETE_NULL_ROWS = """DELETE FROM school
                                    WHERE zoho_secondary_id IS NULL OR zoho_primary_id IS NULL OR secondary_school_name IS NULL OR primary_school_name IS NULL;"""
                crsc.execute(DELETE_NULL_ROWS)
                connection.commit()
                             
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

