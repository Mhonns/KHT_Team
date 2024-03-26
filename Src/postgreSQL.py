from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import geojson
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import mapping
import json
from village_url_model import village_url_data  

# Database configurations
db_host = "127.0.0.1" # "103.153.118.77"
db_port = "5432" # "2547"
db_name = "mhs_geographic"
db_user = "postgres"
db_password = "postgres"

# Connection parameters
connection_params = {
    "host": db_host,
    "port": db_port,
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
}

def query_to_geojson(cursor, query):
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    features = []
    for row in results:
        properties = dict(zip(columns, row))
        geometry_key = 'geom'
        geometry_str = properties.get(geometry_key)
        if geometry_str is not None:
            try:
                # Convert the hex WKB to a Shapely geometry
                geometry = wkb.loads(geometry_str, hex=True)
                # Convert the Shapely geometry to GeoJSON
                geometry_geojson = mapping(geometry)
                feature = geojson.Feature(properties=properties, geometry=geometry_geojson)
                features.append(feature)
            except (json.JSONDecodeError, ValueError):
                print(f"Invalid GeoJSON string: {geometry_str}")

    feature_collection = geojson.FeatureCollection(features)
    # geojson_result = geojson.dumps(feature_collection, indent=2)
    return feature_collection

# Query all data into json format
def query_to_json(cursor, query):
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()
    features = []
    for row in results:
        properties = dict(zip(columns, row))
        feature = {"properties": properties}
        features.append(feature)
    feature_collection = {"type": "FeatureCollection", "features": features}
    # json_result = json.dumps(feature_collection, indent=2)
    return feature_collection

# Query all column datail
# def get_table(target_table, geojson_format=True, argument=""):
#     # Example query
#     query = None
#     if argument == "":
#         query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(target_table))
#     elif target_table == "project":
#         query = sql.SQL("""SELECT DISTINCT project.id,project_name_en,start_date,end_date,projectvillage.village_id 
#                            FROM {} 
#                            JOIN projectvillage ON projectvillage.project_id = project.id
#                            WHERE village_id = {}::uuid""").format(sql.Identifier(target_table), sql.Literal(argument))

#     try:
#         cursor.execute(query)
#         results = None
#         if geojson_format:
#             geojson_result = query_to_geojson(cursor, query)
#             return geojson_result
#         else:
#             json_result = query_to_json(cursor, query)
#             return json_result
#     except:
#         print(f"Error executing query")
#         connection.rollback()  # Rollback the transaction

# Query village
def get_village(village_id=""):
    query = None
    if village_id == "":
        query = sql.SQL("SELECT * FROM village")
    else:
        query = sql.SQL("SELECT * FROM village WHERE id = {}").format(sql.Literal(village_id))
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Query project
def get_project(village_id="", start_year="", end_year=""):
    query = None
    if village_id == "":
        if start_year == "":
            start_year = -1
        if end_year == "":
            end_year = 9999
        query = sql.SQL("""SELECT project.*, projectStatus.status_name
                            FROM project 
                            JOIN projectStatus ON project.status_id = projectStatus.status_id
                            WHERE start_date >= {} 
                            AND end_date <= {}""").format(sql.Literal(str(start_year)), sql.Literal(str(end_year)))
    else:
        query = sql.SQL("""SELECT DISTINCT project.id,project_name_en,start_date,end_date,project_type, projectStatus.status_name, projectvillage.village_id
                            FROM project
                            JOIN projectvillage ON projectvillage.project_id = project.id
                            JOIN projectStatus ON project.status_id = projectStatus.Status_id
                            WHERE village_id = {}::uuid""").format(sql.Literal(village_id))
    try:
        cursor.execute(query)
        json_result = query_to_json(cursor, query)
        return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Query village project by year
def get_village_project_by_year(year="", start_year="", end_year=""):
    query = None
    print(year, start_year, end_year)
    if year:
        start_year = year
        end_year = year
    query = sql.SQL("""SELECT village.*, projectStatus.status_name
                        FROM village
                        JOIN projectvillage ON projectvillage.village_id = village.id
                        JOIN project ON project.id = projectvillage.project_id
                        JOIN projectStatus ON project.status_id = projectStatus.status_id
                        WHERE project.start_date >= {} 
                        AND project.end_date <= {}""").format(sql.Literal(str(start_year)), sql.Literal(str(end_year)))
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Query project type
def get_project_type(project_type=""):
    query = None 
    query = sql.SQL("""SELECT village.*
                        FROM village
                        JOIN projectvillage ON projectvillage.village_id = village.id
                        JOIN project ON project.id = projectvillage.project_id
                        WHERE project.project_type = {}""").format(sql.Literal(project_type))
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction


def get_project_donor(project_id=""):
    query = None
    query = sql.SQL("""SELECT donor.id,donor.donator_name
                        FROM donor
                        JOIN projectdonor ON projectdonor.donor_id = donor.id
                        WHERE projectdonor.project_id= {}::uuid""").format(sql.Literal(project_id))
    try:
        cursor.execute(query)
        json_result = query_to_json(cursor, query)
        return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_hospital():
    query = None
    query = sql.SQL("SELECT * FROM hospital")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_school():
    query = None
    query = sql.SQL("SELECT * FROM school")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_districts():
    query = None
    query = sql.SQL("SELECT * FROM mhs_districts")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_roads():
    query = None
    query = sql.SQL("SELECT * FROM mhs_roads")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_water_ares():
    query = None
    query = sql.SQL("SELECT * FROM mhs_water_areas")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

def get_mhs_water_lines():
    query = None
    query = sql.SQL("SELECT * FROM mhs_water_lines")
    try:
        cursor.execute(query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction 

def get_village_from_distance(distance="", facility_type="", facility_name=""):
    query = None
    # facility_type = "hospital"
    # facility_name = "โรงพยาบาลส่งเสริมสุขภาพตำบลสล่าเชียงตอง"
    # distance = 5000
    print(distance)
    print(facility_type)
    print(facility_name)
    print(sql.Literal(facility_name)) 

    query = sql.SQL("""SELECT * from {table}""").format(table=sql.Identifier(facility_type))

    try:
        cursor.execute(query)
        full_query = query.as_string(cursor)
        print(full_query)
        geojson_result = query_to_geojson(cursor, query)
        return geojson_result
    except:
        print(f"Error executing query")
        connection.rollback()
    
    # query = sql.SQL("""
    #     SELECT village.*
    #     FROM village
    #     JOIN {table} ON {table}.{column} = {facility_name}
    #     AND ST_DWithin(village.geom::geography, {table}.geom::geography, %s)
    # """).format(table=sql.Identifier(facility_type),
    #             column=sql.Identifier(facility_type + "_name"),
    #             facility_name=sql.Literal(facility_name))

    # try:
    #     cursor.execute(query, (distance,))
    #     full_query = query.as_string(cursor)
    #     print(full_query)
    #     geojson_result = query_to_geojson(cursor, query)
    #     return geojson_result
    # except:
    #     print(f"Error executing query")
    #     connection.rollback()  # Rollback the transaction

def insert_village_url(village_url_data):
    print(village_url_data)
    query = None
    query = sql.SQL("""
        INSERT INTO url2 (village_name, url, image_url, article_title, posted_date, created_time)
        SELECT %s, %s, %s, %s, %s, CAST(TO_CHAR(NOW()::date, 'DD/MM/YYYY') AS VARCHAR(256))
        WHERE EXISTS (
            SELECT 1
            FROM village
            WHERE village.village_name = %s
        )
    """)
    try:
        cursor.execute(query, (village_url_data.village_name, village_url_data.url, village_url_data.image_url, village_url_data.article_title, village_url_data.posted_date, village_url_data.village_name ))
        rows_inserted = cursor.rowcount
        connection.commit()
        if cursor.rowcount == 0:
            print(f"Data not inserted into url table. {rows_inserted} rows inserted.")
            message = {
                "status": "Failed",
                "message": f"Village '{village_url_data.village_name}' not found in village table. Data not inserted into url table."
            }
        else:
            print(f"Data inserted into url table. {rows_inserted} rows inserted.")
            message = {
                "status": "Success",
                "message": f"Village '{village_url_data.village_name}' found in village table. Data inserted into url table."
            }
    except Exception as e:
        print(f"Error executing query: {e}")
        connection.rollback()
    return message
   
# update url table
def update_url_table2():
    try:
        # Define a SQL query to update the 'village_id' column in the 'url2' table
        UPDATE_VILLAGE_ID = """
            UPDATE url2
            SET village_id = village.id  -- Set 'village_id' to the 'id' of the matching 'village' row
            FROM village  -- Join with the 'village' table
            WHERE url2.village_name = village.village_name;  -- Match rows based on the 'village_name' column
        """
        cursor.execute(UPDATE_VILLAGE_ID)
        connection.commit()
        print('Village IDs updated successfully.')

        # Define a SQL query to update the 'sequence' column in the 'url2' table
        UPDATE_SEQUENCE = """
            -- Create a Common Table Expression (CTE) named 'cte'
            WITH cte AS (
                -- Select the 'id' and the row number within each 'village_name' group
                SELECT id, ROW_NUMBER() OVER(PARTITION BY village_name ORDER BY posted_date) AS rn
                FROM url2
            )
            -- Update the 'sequence' column in the 'url2' table
            UPDATE url2
            SET sequence = cte.rn  -- Set 'sequence' to the row number within each 'village_name' group
            FROM cte  -- Use the 'cte' CTE in the UPDATE statement
            WHERE url2.id = cte.id;  -- Only update rows where the 'id' matches between the 'url2' table and the 'cte' CTE
        """
        cursor.execute(UPDATE_SEQUENCE)
        connection.commit()
        print('Sequence numbers updated successfully.')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if connection is not None:
            connection.rollback()
            print('Error occurred. Rolling back changes.')

# Establish a connection to the database
try:
    connection = psycopg2.connect(**connection_params)
    print("Connected to the database!")
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")

def close_all():
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")
