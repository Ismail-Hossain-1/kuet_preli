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


