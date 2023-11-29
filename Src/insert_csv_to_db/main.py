import os
import psycopg2
from config import config
from create_projectVillage_table import create_projectVillage_table
from create_project_table import create_project_table # Connect to the database
from create_village_table import create_village_table
from create_projectStatus_table import create_projectStatus_table
from get_village_table import get_village_table

def connect():
    connection = None

    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()

        ## Add tables here ##
        # create_village_table()
        # create_projectStatus_table()
        # create_project_table()
        get_village_table()
       
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
    # create_village_table()
    # create_projectStatus_table()
    # create_project_table()
    # create_projectVillage_table()
    get_village_table()
    connect()






