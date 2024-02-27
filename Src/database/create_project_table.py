import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config
import pandas as pd

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_project_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        crsc = connection.cursor() 

        CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS projectTest (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                project_name_en VARCHAR(256),
                zoho_project_type_id VARCHAR(256),
                created_time VARCHAR(256),
                start_date VARCHAR(256),
                end_date VARCHAR(256),
                donor1_id VARCHAR(256),
                donor3_id VARCHAR(256),
                donor2_id VARCHAR(256),
                zoho_village_id VARCHAR(256),
                status VARCHAR(256)
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        input_file_path = get_file_path('Data/Project_Cases_001.csv')
        output_file_path = get_file_path('project_001.csv')

        columns_to_select = ['Solution Title', 'Product Name.id', 'Created Time', 'Project Start Date', 'Project End Date', 'Donor 1 (D1) Id', 'Donor 3 (D3) Id', 'Donor 2 (D2) Id', 'Village Id', 'Project Type']

        # Select columns and save to a  new CSV file
        select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

        # Fetch the 'created_time' column from the 'project' table
        crsc.execute("SELECT created_time FROM projectTest;")
        existing_times = [item[0] for item in crsc.fetchall()]

        # Load the new CSV data into a DataFrame
        new_data = pd.read_csv(output_file_path)

        # Filter the new data to only include rows with 'created_time' values that don't exist in the database
        new_data = new_data[~new_data['created_time'].isin(existing_times)]
       
        # If there are no new rows, print a message and return
        if new_data.empty:
            print('\nNo new rows to add to the project table.')
        else:
            print('\nAdding new rows to the project table...')
            num_rows_added = len(new_data)
            print(f'{num_rows_added} rows added.')

        # Save the filtered data to a new CSV file
        new_data.to_csv(output_file_path, index=False)

        # Use 'copy_expert' to copy the new data from the CSV file into the 'project' table
        with open(output_file_path, 'r') as f:
            next(f)  # Skip the header
            crsc.copy_expert(
                "COPY projectTest (project_name_en, zoho_project_type_id, created_time, start_date, end_date, donor1_id, donor3_id, donor2_id, zoho_village_id, status) FROM STDIN WITH CSV DELIMITER ',' QUOTE '\"' NULL 'null'",
                f
            )
        connection.commit()    

        # add column for status_id  
        ADD_PROJECTSTATUS_COLUMN = """ALTER TABLE projectTest
            ADD COLUMN status_id INTEGER REFERENCES projectStatus (status_id);"""
        crsc.execute(ADD_PROJECTSTATUS_COLUMN)
        connection.commit()

        # Update the 'status_id' column based on the values from the projectStatus table
        UPDATE_STATUS_ID = """
            UPDATE projectTest
            SET status_id = projectStatus.status_id
            FROM projectStatus
            WHERE projectTest.status = projectStatus.status_name;
        """
        crsc.execute(UPDATE_STATUS_ID)
        connection.commit()

        # Drop the old 'status' column
        DROP_STATUS_COLUMN = """ALTER TABLE projectTest
                                    DROP COLUMN status;"""
        crsc.execute(DROP_STATUS_COLUMN)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
