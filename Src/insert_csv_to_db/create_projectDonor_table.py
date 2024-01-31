import os
import psycopg2
from config import config
from clean_csv import select_2_columns_and_save_csv

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

def create_projectDonor_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        crsc = connection.cursor()
       
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS projectDonor (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                project_id UUID,
                donor_id UUID,
                FOREIGN KEY (project_id) REFERENCES projectTest(id),
                FOREIGN KEY (donor_id) REFERENCES donor(id)
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        # """
        # INSERT INTO projectVillageTest (village_id, project_id)
        # SELECT villagetest.id AS village_id, projecttest.id AS project_id
        # FROM projecttest
        # JOIN villagetest ON projecttest.zoho_village_id = villagetest.record_id;"""

        INSERT_TO_PROJECTDONOR_TABLE_DONOR1 = """
        INSERT INTO projectDonor (project_id, donor_id)
        SELECT projectTest.id AS project_id, donor.id AS donor_id
        FROM projectTest
        JOIN donor ON projectTest.donor1_id = donor.record_id
        """
        crsc.execute(INSERT_TO_PROJECTDONOR_TABLE_DONOR1)
        connection.commit()

        INSERT_TO_PROJECTDONOR_TABLE_DONOR2 = """
        INSERT INTO projectDonor (project_id, donor_id)
        SELECT projectTest.id AS project_id, donor.id AS donor_id
        FROM projectTest
        JOIN donor ON projectTest.donor2_id = donor.record_id
        """
        crsc.execute(INSERT_TO_PROJECTDONOR_TABLE_DONOR2)
        connection.commit()

        INSERT_TO_PROJECTDONOR_TABLE_DONOR3 = """
        INSERT INTO projectDonor (project_id, donor_id)
        SELECT projectTest.id AS project_id, donor.id AS donor_id
        FROM projectTest
        JOIN donor ON projectTest.donor3_id = donor.record_id
        """
        crsc.execute(INSERT_TO_PROJECTDONOR_TABLE_DONOR3)
        connection.commit()
                                            
        print('\nprojectDonor table created successfully.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')
