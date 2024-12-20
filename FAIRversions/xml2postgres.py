import psycopg2
import chardet

# Database connection settings
db_config = {
    "dbname": "myxmlfilesdb",
    "user": "myfastapiuser",
    "password": "mypassword",
    "host": "localhost"
}

# Path to your XML file
file_path = r'G:\SIR_Data_Management\Digital_database\FAIRversions\Mn-54_database_FAIR.xml'

# Read the XML file content and clean it
try:
    # Detect file encoding
    with open(file_path, 'rb') as raw_file:
        raw_data = raw_file.read()

    result = chardet.detect(raw_data)
    detected_encoding = result['encoding']
    print(f"Detected file encoding: {detected_encoding}")

    # Decode using detected encoding and re-encode in UTF-8
    xml_content = raw_data.decode(detected_encoding, errors='replace')  # Replace any bad chars
    xml_content_utf8 = xml_content.encode('utf-8', errors='ignore').decode('utf-8')  # Clean it further

    print("XML file read successfully and converted to UTF-8!")

except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit(1)
except UnicodeDecodeError as e:
    print(f"Unicode decoding error: {e}")
    exit(1)
except Exception as e:
    print(f"Error reading XML file: {e}")
    exit(1)

# Connect to the PostgreSQL database
conn = None
try:
    # Attempt to connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Insert the XML file content into the table
    insert_query = """
        INSERT INTO xml_files (filename, xml_content)
        VALUES (%s, %s)
    """
    cur.execute(insert_query, ('Mn-54_database_FAIR.xml', xml_content_utf8))

    # Commit the transaction
    conn.commit()
    print("File inserted successfully!")

except psycopg2.OperationalError as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

except Exception as e:
    print(f"Error during file insertion: {e}")
    if conn:
        conn.rollback()  # Rollback in case of any error during insertion

finally:
    # Ensure that the cursor and connection are closed
    if conn:
        cur.close()
        conn.close()
        print("Database connection closed.")
