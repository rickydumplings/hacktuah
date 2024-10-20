from flask import Flask, jsonify, request
import singlestoredb as s2  # Use singlestoredb instead of pymysql for consistency

app = Flask(__name__)

# Configure your SingleStore connection
def get_singlestore_connection():
    return s2.connect('rick-ca315:Aashurith!@svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com:3333/db_rick_9d7b1')

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Establish the connection
        connection = get_singlestore_connection()

        # Create a cursor
        cursor = connection.cursor()

        # Query to get data from your table
        query = "SELECT location, name, summary, actions FROM entities"
        cursor.execute(query)

        # Fetch all the results
        result = cursor.fetchall()

        # Close the connection
        connection.close()

        # Convert the result into a list of dictionaries
        data = []
        for row in result:
            data.append({
                'location': row[0],
                'name': row[1],
                'summary': row[2],
                'actions': row[3]
            })

        # Return the result as JSON
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)