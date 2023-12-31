import psycopg2
import geojson
from psycopg2 import sql
from shapely import wkb
from shapely.geometry import mapping
import json

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
    # cursor.execute(query)
    # columns = [desc[0] for desc in cursor.description]
    # results = cursor.fetchall()

    # features = []
    # for row in results:
    #     properties = dict(zip(columns, row))
    #     geometry = properties.pop('geom', None)  # Assuming 'geometry' is the column name for geometry data
    #     feature = geojson.Feature(properties=properties, geometry=geometry)
    #     features.append(feature)

    # feature_collection = geojson.FeatureCollection(features)
    # return geojson.dumps(feature_collection, indent=2)
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
def get_table(target_table, geojson_format=True, argument=""):
    # Example query
    query = None
    if argument == "":
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(target_table))
    elif target_table == "project":
        query = sql.SQL("""SELECT DISTINCT project.id,project_name_en,start_date,end_date,projectvillage.village_id 
                           FROM {} 
                           JOIN projectvillage ON projectvillage.project_id = project.id
                           WHERE village_id = {}::uuid""").format(sql.Identifier(target_table), sql.Literal(argument))

    try:
        cursor.execute(query)
        results = None
        if geojson_format:
            geojson_result = query_to_geojson(cursor, query)
            return geojson_result
        else:
            json_result = query_to_json(cursor, query)
            return json_result
    except:
        print(f"Error executing query")
        connection.rollback()  # Rollback the transaction

# Establish a connection to the database
try:
    connection = psycopg2.connect(**connection_params)
    print("Connected to the database!")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    # print(get_table("project", False))
    # print(get_table("village"))

except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")

def close_all():
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")

