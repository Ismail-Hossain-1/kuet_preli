from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
# Load environment variables from .env file
load_dotenv()


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
    model_name= 'gemini-1.5-flash', system_instruction="",
    tools=[]
            )

chat_history=[]

chat= model.start_chat(history=chat_history, enable_automatic_function_calling=True)

@app.route('/', methods=['GET'])
def hello_world():
    
    return 'Hello, World!'




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


