import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

# join folder called 'Data' and file called 'Villages_001.csv'
input_file_path = get_file_path('Data\Villages_001.csv')
output_file_path = get_file_path('villages_001.csv')

columns_to_select = ['Village Name', 'Households', 'Road Conditions', 'Total Population', 'GPS Latitude',
    'GPS Longitude', '% Population Without Enough Rice', 'Children (Aged 0 - 18)',
    'Distance to Town (km)', 'Adult Males', 'Adult Females', 'Distance to Hospital (km)',
    'Nearest Health Centre', 'Distance to Pratom (km)', 'Annual Typhoid Cases',
    'Distance to Health Centre (km)', 'Distance to Mathayom (km)', 'Common Diseases',
    'Hosted KHT Projects', 'Record Id']

select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

def create_village_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()
       
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS villagetest2 (
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
                hosted_kht_projects VARCHAR(256),
                record_id VARCHAR(256)
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        # insert the other columns other than the id column
        with open(output_file_path, 'r') as f:
            next(f)
            crsc.copy_expert(
                "COPY villagetest2 (village_name, households, road_conditions, total_population, gps_latitude, gps_longitude, population_without_enough_rice, children_aged_0_18, distance_to_town_km, adult_males, adult_females, distance_to_hospital_km, nearest_health_centre, distance_to_pratom_km, annual_typhoid_cases, distance_to_health_centre_km, distance_to_mathayom_km, common_diseases, hosted_kht_projects, record_id) FROM STDIN WITH CSV HEADER",
            f
        )
        connection.commit()    

        # Remove any rows where latitude or longitude is null
        crsc.execute("""DELETE FROM villagetest2 WHERE gps_latitude IS NULL OR gps_longitude IS NULL;""")
        connection.commit()

        # add a geom column to the table with a point geometry type from columns gps_latitude and gps_longitude
        crsc.execute("""ALTER TABLE villagetest2
            ADD COLUMN geom geometry(Point, 4326);""")
        connection.commit()

        # update the geom column with the point geometry type from columns gps_latitude and gps_longitude
        crsc.execute("""UPDATE villagetest2
            SET geom = ST_SetSRID(ST_MakePoint(gps_longitude, gps_latitude), 4326);""")
        connection.commit()

        print('Village table created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    create_village_table()
