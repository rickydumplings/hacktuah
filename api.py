from flask import Flask, jsonify
import singlestoredb as s2

app = Flask(__name__)

# Connection string for SingleStore (as per your script)
def get_singlestore_connection():
    try:
        conn = s2.connect('rick-ca315:Aashurith!@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_rick_9d7b1')
        return conn
    except Exception as e:
        print(f"Error connecting to SingleStore: {e}")
        return None

# API route to fetch all data from 'entities' table
@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_singlestore_connection()
    if not conn:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        with conn.cursor() as cur:
            query = "SELECT label, value FROM entities"
            cur.execute(query)
            result = cur.fetchall()
        
        # Format result as a list of dictionaries
        data = [{'label': row[0], 'value': row[1]} for row in result]
        
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching data from SingleStore: {e}")
        return jsonify({'error': 'Failed to fetch data'}), 500
    finally:
        conn.close()

# Run the Flask app with SSL (for HTTPS)
if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # For development; for production use proper SSL certificates
