import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config
import pandas as pd

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_hospital_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        with psycopg2.connect(**params) as connection:
            with connection.cursor() as crsc:
                # create hospital table if it does not exist
                CREATE_TABLE = """CREATE TABLE IF NOT EXISTS hospital (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        village_name VARCHAR(256),
                        created_time VARCHAR(256),
                        hospital_name VARCHAR(256)
                    );"""
                crsc.execute(CREATE_TABLE)

                # Input and output file paths
                input_file_path = get_file_path('Data/Villages_001.csv')
                output_file_path = get_file_path('hospitals.csv')

                # Select columns and save to a new CSV file
                columns_to_select = ['Village Name', 'Created Time', 'Nearest Health Centre']

                select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

                # Fetch the 'created_time' column from the 'hospitaltest' table
                crsc.execute("SELECT created_time FROM hospital;")
                existing_times = [item[0] for item in crsc.fetchall()]

                # Load the new CSV data into a DataFrame
                new_data = pd.read_csv(output_file_path)

                # Filter the new data to only include rows with 'created_time' values that don't exist in the database
                new_data = new_data[~new_data['created_time'].isin(existing_times)]

                # If there are no new rows, print a message and return
                if new_data.empty:
                    print('No new rows to add.')
                else:
                    print('Adding new rows to the hospital table...')

                # Save the filtered data to a new CSV file
                new_data.to_csv(output_file_path, index=False)

                # Use 'copy_expert' to copy the new data from the CSV file into the 'hospitaltest' table
                with open(output_file_path, 'r') as f:
                    next(f)  # Skip the header
                    crsc.copy_expert(
                        "COPY hospital (village_name, created_time, hospital_name) FROM STDIN WITH CSV HEADER",
                        f
                    )
                connection.commit()       

                # Remove null values from the hospital_name column
                DELETE_NULL_ROWS = """DELETE FROM hospital WHERE hospital_name IS NULL;"""
                crsc.execute(DELETE_NULL_ROWS)
                connection.commit()
                             
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')