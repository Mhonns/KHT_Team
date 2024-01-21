import os
import psycopg2
from config import config
from clean_csv import select_2_columns_and_save_csv

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_projectVillage_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        crsc = connection.cursor()
       
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS projectVillageTest (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                village_id UUID,
                project_id UUID 
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        INSERT_TO_PROJECTVILLAGE_TABLE = """INSERT INTO projectVillageTest (village_id, project_id)
                                            SELECT villagetest.id AS village_id, projecttest.id AS project_id
                                            FROM projecttest
                                            JOIN villagetest ON projecttest.zoho_village_id = villagetest.record_id;"""
        crsc.execute(INSERT_TO_PROJECTVILLAGE_TABLE)
        connection.commit()
                                            
        print('\nprojectVillage table created successfully.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')





