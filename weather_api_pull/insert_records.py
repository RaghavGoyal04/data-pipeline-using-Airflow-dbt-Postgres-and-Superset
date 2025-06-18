from psycopg2 import connect, sql, Error
import sys 

def connect_to_db():
    try:
        # Connect to the PostgreSQL database
        conn = connect(
            host="db", # Use the service name defined in docker-compose
            port=5432, # Default PostgreSQL port in docker-compose
            dbname="weather_db",
            user="user",
            password="password",
        )
        # Check if the connection is successful
        if conn is not None:
            print("Connection to the database established successfully.")
            return conn
        else:
            print("Failed to connect to the database.")
        # Return the connection object
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise

def drop_weather_table(schema_name='dev', table_name='raw_weather_data'):
    print(f"Dropping '{table_name}' table if exists...")

    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            # Drop the specified table if it exists
            drop_table_query = sql.SQL(f"""
                DROP TABLE IF EXISTS {schema_name}.{table_name};
            """).format(schema_name=sql.Identifier(schema_name), table_name=sql.Identifier(table_name))
            cursor.execute(drop_table_query)
            conn.commit()
            print(f"Table '{table_name}' dropped successfully.")

    except Error as e:
        print(f"Error dropping table: {e}")
        raise
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def create_weather_table(schema_name='dev', table_name='raw_weather_data'):
    print(f"Creating '{schema_name}.{table_name}' table if not exists...")

    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            # Create the weather_data table if it doesn't exist
            create_table_query = sql.SQL(f"""
                CREATE SCHEMA IF NOT EXISTS {schema_name};
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100) NOT NULL,
                    main_weather VARCHAR(50) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    temperature FLOAT NOT NULL,
                    wind_speed FLOAT,
                    wind_direction FLOAT,
                    humidity INT,
                    pressure INT,
                    visibility INT,
                    utc_offset BIGINT,
                    dt BIGINT,
                    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table '{schema_name}.{table_name}' created successfully.")

    except Error as e:
        print(f"Error creating table: {e}")
        raise
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


def insert_weather_data(data, schema_name='dev', table_name='raw_weather_data'):
    # Connect to the database
    print(f"Inserting weather data into '{schema_name}.{table_name}' table...")
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            # Create the insert query
            insert_query = sql.SQL("""
                INSERT INTO {schema_name}.{table_name} (city, main_weather, description, temperature, wind_speed, wind_direction, humidity, pressure, visibility, utc_offset, dt, inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """).format(schema_name=sql.Identifier(schema_name), table_name=sql.Identifier(table_name))

            # Execute the insert query
            main = data['main']
            cursor.execute(insert_query, (data['name'], data['weather'][0]['main'],  data['weather'][0]['description'], main['temp'], data['wind']['speed'], data['wind']['deg'], main['humidity'], main['pressure'], data['visibility'], data['timezone'], data['dt']))
            print("Weather data inserted successfully.")

            # Commit the transaction
            conn.commit()

    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
