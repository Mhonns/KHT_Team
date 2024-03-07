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
                #ชื่อหน่วยงาน,จังหวัด,อำเภอ,ตำบล,FormattedAddress,LAT_LON
                CREATE_TABLE = """CREATE TABLE IF NOT EXISTS hospital (
                        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                        hospital_name VARCHAR(255),
                        province VARCHAR(255),
                        district VARCHAR(255),
                        sub_district VARCHAR(255),
                        postal_code VARCHAR(255),
                        formatted_address VARCHAR(255),
                        gps_latitude DOUBLE PRECISION,
                        gps_longitude DOUBLE PRECISION,
                        geom geometry(Point, 4326),
                        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );"""
                crsc.execute(CREATE_TABLE)

                # Input and output file paths
                input_file_path = get_file_path('Data/complete_hospital_data_p1.csv')
                output_file_path = get_file_path('hospitals.csv')

                # hospital_name,province,district,sub_district,postal_code,formatted_address,gps_latitude,gps_longitude
                # Select columns and save to a new CSV file
                columns_to_select = ['hospital_name', 'province', 'district', 'sub_district', 'postal_code', 'formatted_address', 'gps_latitude', 'gps_longitude']

                select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

                # Load the new CSV data into a DataFrame
                new_data = pd.read_csv(output_file_path)

                 # Fetch the existing timestamps from the database
                crsc.execute("SELECT created_time FROM hospital;")
                existing_times = [item[0] for item in crsc.fetchall()]

                # Convert the existing_times to pandas datetime for comparison
                existing_times = pd.to_datetime(existing_times)

                # Filter out the rows in new_data that have a created_time in existing_times
                new_data = new_data[~new_data['created_time'].isin(existing_times)]

                # If there are no new rows, print a message and return
                if new_data.empty:
                    print('No new rows to add.')
                    return
                else:
                    print('Adding new rows to the hospital table...')

                # Save the filtered data to a new CSV file
                new_data.to_csv(output_file_path, index=False)

                # Use 'copy_expert' to copy the new data from the CSV file into the 'hospitaltest' table
                with open(output_file_path, 'r') as f:
                    next(f)  # Skip the header
                    crsc.copy_expert(
                        "COPY hospital (hospital_name, province, district, sub_district, postal_code, formatted_address, gps_latitude, gps_longitude) FROM STDIN WITH CSV HEADER",
                        f
                    )
                connection.commit()     

                UPDATE_CREATED_TIME = """UPDATE hospital SET created_time = CURRENT_TIMESTAMP WHERE created_time IS NULL;"""
                crsc.execute(UPDATE_CREATED_TIME)
                connection.commit()

                # Set the SRID of the 'geom' column to 4326
                SET_GEOM_SRID = """UPDATE hospital SET geom = ST_SetSRID(ST_MakePoint(gps_longitude, gps_latitude), 4326);"""
                crsc.execute(SET_GEOM_SRID)

                print('Hospital table created successfully.')
                             
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')