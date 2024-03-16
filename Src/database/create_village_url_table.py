import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config
import pandas as pd

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_village_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        with psycopg2.connect(**params) as connection:
            with connection.cursor() as crsc:
                # create village table if it does not exist
                CREATE_TABLE = """CREATE TABLE IF NOT EXISTS villageUrl (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        village_id, UUID,
                        url, VARCHAR(256),
                        village_name VARCHAR(256),
                        entered_date VARCHAR(256),
                        sequence INT,
                        article_title VARCHAR(256),
                        posted_date VARCHAR(256)
                    );"""
                crsc.execute(CREATE_TABLE)

                # Input and output file paths
                input_file_path = get_file_path('Data/village_url.csv')
                output_file_path = get_file_path('village_url.csv')

                # Select columns and save to a  new CSV file
                columns_to_select = ['village_name', 'url', 'article_Stitle', 'posted_date','entered_date']
                
                columns_to_convert = ['village_name', 'url', 'article_title', 'posted_date','entered_date']

                select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select, columns_to_convert)

                # Fetch the 'created_time' column from the 'village' table
                crsc.execute("SELECT created_time FROM villageUrl;")
                existing_times = [item[0] for item in crsc.fetchall()]

                # Load the new CSV data into a DataFrame
                new_data = pd.read_csv(output_file_path)

                # Filter the new data to only include rows with 'created_time' values that don't exist in the database
                new_data = new_data[~new_data['created_time'].isin(existing_times)]
                
                # If there are no new rows, print a message and return
                if new_data.empty:
                    print('\nNo new rows to add to the villageUrl table.')
                else:
                    print('\nAdding new rows to the villageUrl table...')
                    num_rows_added = len(new_data)
                    print(f'{num_rows_added} rows added.')

                # Save the filtered data to a new CSV file
                new_data.to_csv(output_file_path, index=False)

                # Use 'copy_expert' to copy the new data from the CSV file into the 'village' table
                with open(output_file_path, 'r') as f:
                    next(f)  # Skip the header
                    crsc.copy_expert(
                        "COPY villageUrl (village_id, url, village_name, entered_date, sequence, article_title, posted_date) FROM STDIN WITH CSV HEADER",  # SQL statement
                        f
                    )
                connection.commit()              
                             
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

