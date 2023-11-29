import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

# join folder called 'Data' and file called 'Villages_001.csv'
input_file_path = get_file_path('Data\Project_Cases_001.csv')
output_file_path = get_file_path('project_001.csv')

columns_to_select = ['Solution Title', 'Project Start Date', 'Project End Date', 'Project Type', 'Village Id']

select_columns_and_save_csv(input_file_path, output_file_path, columns_to_select)

def create_project_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()
       
        CREATE_TABLE = """CREATE TABLE IF NOT EXISTS project (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                project_name_en VARCHAR(256),
                start_date VARCHAR(256),
                end_date VARCHAR(256),
                status VARCHAR(256)
            );"""
        crsc.execute(CREATE_TABLE)
        connection.commit()

        # insert the other columns other than the id column
        with open(output_file_path, 'r') as f:
            next(f)
            crsc.copy_expert(
                "COPY project (project_name_en, start_date, end_date, status) FROM STDIN WITH CSV HEADER",
                f
            )
        connection.commit()    

        # add column for status_id  
        crsc.execute("""ALTER TABLE project 
            ADD COLUMN status_id INTEGER REFERENCES projectStatus (status_id);""")
        connection.commit()

        # Update the 'status_id' column based on the values from the projectStatus table
        crsc.execute("""
            UPDATE project
            SET status_id = projectStatus.status_id
            FROM projectStatus
            WHERE project.status = projectStatus.status_name;
        """)
        connection.commit()

        # Drop the old 'status' column
        ALTER_TABLE_DROP_COLUMN = """ALTER TABLE project
                                    DROP COLUMN status;"""
        crsc.execute(ALTER_TABLE_DROP_COLUMN)
        connection.commit()

        print('Project table created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    create_project_table()
