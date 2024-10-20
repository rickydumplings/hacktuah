import singlestoredb as s2
import json

# Path to your JSON file
json_file_path = 'cleaned_entities.json'

# Create a connection to the database
try:
    conn = s2.connect('rick-ca315:Aashurith!@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_rick_9d7b1')
except Exception as e:
    print(f"Error connecting to SingleStore: {e}")
    exit()

# Function to delete prior data and insert new data into SingleStore
def upload_data_to_singlestore(conn, data):
    try:
        with conn:
            with conn.cursor() as cur:
                # Step 1: Delete all existing data from the table
                delete_query = "DELETE FROM entities"
                cur.execute(delete_query)
                print("All prior data deleted.")

                # Step 2: Insert new data
                for record in data:
                    label = record.get('label')
                    value = record.get('value')
                    insert_query = "INSERT INTO entities (label, value) VALUES (%s, %s)"
                    cur.execute(insert_query, (label, value))

                # Commit the transaction
                conn.commit()
        print("New data uploaded successfully!")
    except Exception as e:
        print(f"Error uploading data to SingleStore: {e}")

# Read the JSON file
try:
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print("JSON file not found.")
    exit()
except json.JSONDecodeError as e:
    print(f"Error reading JSON file: {e}")
    exit()

# Upload the data to SingleStore, replacing the prior contents
upload_data_to_singlestore(conn, json_data)
