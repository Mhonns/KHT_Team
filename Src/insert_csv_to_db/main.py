# Example usage
input_file_path = 'C:/Users/panuo/OneDrive/Documents/aaSchool_Work/KHT_RnD_y2s1/ZohoData_python/Data/Villages_001.csv'
output_file_path = 'C:/Users/panuo/OneDrive/Documents/aaSchool_Work/KHT_RnD_y2s1/ZohoData_python/Data/insert_csv_to_db/villages_001.csv'
columns_to_select = ['Village Name', 'Households', 'Road Conditions', 'Total Population', 'GPS Latitude',
    'GPS Longitude', '% Population Without Enough Rice', 'Children (Aged 0 - 18)',
    'Distance to Town (km)', 'Adult Males', 'Adult Females', 'Distance to Hospital (km)',
    'Nearest Health Centre', 'Distance to Pratom (km)', 'Annual Typhoid Cases',
    'Distance to Health Centre (km)', 'Distance to Mathayom (km)', 'Common Diseases',
    'Hosted KHT Projects']

import psycopg2
from clean_csv import select_columns_and_save_csv #python postgresql adapter
from config import config # Connect to the database

    # cursor.execute('SELECT * FROM mhs_roads') # query to be executed
    # rows = cursor.fetchall() # fetch all rows from the result of the query
    # for row in rows:
    #     print(row)

select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

def connect():
    connection = None

    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()

        #create table called village_001
        #with these columns village_name,households,road_conditions,total_population,gps_latitude,gps_longitude,%_population_without_enough_rice,children_aged_0_-_18,distance_to_town_km,adult_males,adult_females,distance_to_hospital_km,nearest_health_centre,distance_to_pratom_km,annual_typhoid_cases,distance_to_health_centre_km,distance_to_mathayom_km,common_diseases,hosted_kht_projects
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS village_001 (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            village_name VARCHAR(256),
            households INTEGER,
            road_conditions VARCHAR(256),
            total_population INTEGER,
            gps_latitude DOUBLE PRECISION,
            gps_longitude DOUBLE PRECISION,
            population_without_enough_rice DOUBLE PRECISION,
            children_aged_0_18 INTEGER,
            distance_to_town_km DOUBLE PRECISION,
            adult_males INTEGER,
            adult_females INTEGER,
            distance_to_hospital_km DOUBLE PRECISION,
            nearest_health_centre VARCHAR(256),
            distance_to_pratom_km DOUBLE PRECISION,
            annual_typhoid_cases INTEGER,
            distance_to_health_centre_km DOUBLE PRECISION,
            distance_to_mathayom_km DOUBLE PRECISION,
            common_diseases VARCHAR(256),
            hosted_kht_projects VARCHAR(256)
        );"""

        crsc.execute(CREATE_TABLE)
        connection.commit()

        # insert the other columns other than the id column
        with open(output_file_path, 'r') as f:
            next(f)
        #     crsc.copy_from(f, 'village_001', sep=',')
        #     connection.commit()
        # crsc.close()  
            crsc.copy_expert(
                "COPY village_001 (village_name, households, road_conditions, total_population, gps_latitude, gps_longitude, population_without_enough_rice, children_aged_0_18, distance_to_town_km, adult_males, adult_females, distance_to_hospital_km, nearest_health_centre, distance_to_pratom_km, annual_typhoid_cases, distance_to_health_centre_km, distance_to_mathayom_km, common_diseases, hosted_kht_projects) FROM STDIN WITH CSV HEADER",
            f
        )
        connection.commit()
            
        print('PostgreSQL database version:')
        crsc.execute('SELECT version()')
        db_version = crsc.fetchone()
        print(db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()






