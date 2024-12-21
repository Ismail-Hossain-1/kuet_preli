from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('host'),           # MySQL server
        user=os.getenv('user'),          # MySQL user
        password=os.getenv('password', ''),  # MySQL password (empty string if not specified)
        database=os.getenv('database')   # Database name you created in phpMyAdmin
    )
    return connection


@app.route('/ingredients', methods=['POST'])
def add_ingredient():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Extract ingredient data from the JSON request
        ingredient_id = data.get('id')
        name = data.get('name')
        quantity = data.get('quantity', 0)
        unit = data.get('unit', 'grams')

        if not ingredient_id or not name:
            return jsonify({"error": "Ingredient ID and Name are required"}), 400

        # Establish MySQL connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the ingredient into the database
        query = """
        INSERT INTO ingredients (id, name, quantity, unit)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (ingredient_id, name, quantity, unit))

        # Commit changes to the database
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({
            "status": "success",
            "message": "Ingredient added successfully"
        }), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({
            "error": "Failed to add ingredient",
            "details": str(e)
        }), 500

