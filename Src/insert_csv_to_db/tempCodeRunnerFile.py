import os
import psycopg2
from clean_csv import select_columns_and_save_csv
from config import config
import geojson
from shapely.geometry import shape
from psycopg2.extras import RealDictCursor
import json
from shapely import wkb
from shapely.geometry import mapping

def get_file_path(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    return file_path

# join folder called 'Data' and file called 'Villages_001.csv'
output_file_path = get_file_path('village.json')

def get_village_table():
    try:    
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)

        crsc = connection.cursor()
       
        GET_VILLAGE = """SELECT * FROM village;"""
        crsc.execute(GET_VILLAGE)
        connection.commit()

        columns = [desc[0] for desc in crsc.description]
        results = crsc.fetchall()

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
        geojson_result = geojson.dumps(feature_collection, indent=2)
        print(geojson_result)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    get_village_table()
