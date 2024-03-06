import os
import psycopg2
from config import config
from create_projectVillage_table import create_projectVillage_table
from create_project_table import create_project_table # Connect to the database
from create_village_table import create_village_table
from create_projectStatus_table import create_projectStatus_table
from get_village_table import get_village_table
from create_donor_table import create_donor_table
from create_projectDonor_table import create_projectDonor_table
from create_project_type_table import create_project_type_table
from create_district_table import create_district_table
from create_school_table import create_school_table
from create_hospital_table import create_hospital_table
from create_village_table_test import create_village_table_test

def connect():
    connection = None

    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()

        # create_projectStatus_table()
        # create_donor_table()
        # create_project_type_table()

        # create_village_table()
        # create_project_table()
        # create_projectVillage_table()
        # create_donor_table()
        # create_projectDonor_table()

        # create_district_table()
        create_hospital_table()
        # create_school_table()

        # create_village_table_test()
       
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






