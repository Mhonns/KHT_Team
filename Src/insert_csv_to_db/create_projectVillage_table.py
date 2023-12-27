import os
import psycopg2
from config import config
from clean_csv import select_2_columns_and_save_csv

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

# for project_table path
project_input_file_path = get_file_path('Data\Project_Cases_001.csv')
# for village_table path
village_input_file_path = get_file_path('Data\Villages_001.csv')

projectVillage_output_file_path = get_file_path('projectVillage_001.csv')
projectVillage_output_file_path_2 = get_file_path('projectVillage_002.csv')

select_2_columns_and_save_csv(project_input_file_path, village_input_file_path, ['Village Id'], ['Record Id'], projectVillage_output_file_path, projectVillage_output_file_path_2)

# for projectVillage_table path
projectVillage_input_file_path = get_file_path('Data\Project_Cases_001.csv')
projectVillage_output_file_path = get_file_path('projectVillage_001.csv')

def create_projectVillage_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()
       
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS projectVillage (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                village_id UUID,
                project_id UUID 
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        INSERT_TO_PROJECTVILLAGE_TABLE = """INSERT INTO projectVillage (village_id, project_id)
                                            SELECT village.id AS village_id, project.id AS project_id
                                            FROM project
                                            JOIN village ON project.zoho_village_id = village.record_id;"""
        crsc.execute(INSERT_TO_PROJECTVILLAGE_TABLE)
        connection.commit()
                                            






        # update the village_id column in the project table from the csv file with column 'Village Id'
        # do not use the projectView table because it does not have the village_id column
        


        
        
        
        
        # Find the where Village Id in project_table is same as Record Id in village_table
        # SELECT * FROM project_table WHERE village_id = (SELECT id FROM village_table WHERE id = village_id)
        # Since I already have columns id in both the project_table and village_table, 
        # insert the id from those that match with the query above into the projectVillage_table

        # SELECT_TABLE = """
        #     SELECT * FROM project 
        #     WHERE temp_village_id = (SELECT id FROM village WHERE id = temp_village_id);
        # """

        # print('projectVillage table created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    create_projectVillage_table()




