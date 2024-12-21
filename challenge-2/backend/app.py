from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
# Load environment variables from .env file
load_dotenv()
import mysql.connector
from dotenv import load_dotenv
import uuid
import datetime
load_dotenv()
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('host'),           # MySQL server
        user=os.getenv('user'),          # MySQL user
        password=os.getenv('password', ''),  # MySQL password (empty string if not specified)
        database=os.getenv('database')   # Database name you created in phpMyAdmin
    )
    return connection




genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

from function_module import *
from ingredients import *

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for specific origin
CORS(app)
model = genai.GenerativeModel('gemini-1.5-flash')


app = Flask(__name__)

# Enable CORS for specific origin
CORS(app)
model = genai.GenerativeModel(
    model_name= 'gemini-1.5-flash', system_instruction="You are a assistant",
    tools=[]
            )

chat_history=[]

chat= model.start_chat(history=chat_history, enable_automatic_function_calling=True)

@app.route('/', methods=['GET'])
def hello_world():
    
    return 'Hello, World!'

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


@app.route('/recipes', methods=['POST'])
def add_recipe():
    try:
        data = request.get_json()
        recipe_id = data.get('id')
        name = data.get('name')
        description = data.get('description', '')
        instructions = data.get('instructions', '')
        taste = data.get('taste', 'savory')
        reviews = data.get('reviews', 0)
        cuisine_type = data.get('cuisine_type', '')
        prep_time = data.get('prep_time', 0)
        is_sweet = data.get('is_sweet', False)

        if not recipe_id or not name:
            return jsonify({"error": "Recipe ID and Name are required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO recipes (id, name, description, instructions, taste, reviews, cuisine_type, prep_time, is_sweet)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (recipe_id, name, description, instructions, taste, reviews, cuisine_type, prep_time, is_sweet))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Recipe added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to add recipe", "details": str(e)}), 500


@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        # Optional filters from query parameters
        taste = request.args.get('taste', '')
        cuisine_type = request.args.get('cuisine_type', '')
        max_prep_time = request.args.get('max_prep_time', type=int)

        query = "SELECT * FROM recipes WHERE 1=1"
        params = []

        if taste:
            query += " AND taste = %s"
            params.append(taste)
        if cuisine_type:
            query += " AND cuisine_type = %s"
            params.append(cuisine_type)
        if max_prep_time:
            query += " AND prep_time <= %s"
            params.append(max_prep_time)

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        recipes = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(recipes)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve recipes", "details": str(e)}), 500
    
    
@app.route('/recipes/<recipe_id>/ingredients', methods=['POST'])
def add_ingredient_to_recipe(recipe_id):
    try:
        data = request.get_json()
        ingredient_id = data.get('ingredient_id')
        quantity_needed = data.get('quantity_needed', 0)
        unit = data.get('unit', 'grams')

        if not ingredient_id or quantity_needed <= 0:
            return jsonify({"error": "Ingredient ID and valid quantity are required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity_needed, unit)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (recipe_id, ingredient_id, quantity_needed, unit))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Ingredient added to recipe successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to add ingredient to recipe", "details": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def ChatController():
    try:
        req = request.get_json()
        prompt= req['message']
        userId= req['user_id']
        user_Id =userId
        
        chat_history.append({
            "role": "user",
            "parts": [
                {"text": prompt},
                {"text": F"user's user id{userId}"}
            ]
        })
        
        chat= model.start_chat(history=chat_history, enable_automatic_function_calling=True)

        response= chat.send_message(prompt)
        ai_text= response.text.replace("**","")    
        
        
        return jsonify({
            'text': ai_text
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    # Run the app on port 8080
    app.run(debug=True, port=5000)


