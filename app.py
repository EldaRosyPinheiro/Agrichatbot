from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
from chatbot.response_generator import AgricultureBot

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for integration with existing websites

# Initialize the agriculture bot
agri_bot = AgricultureBot()

@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Generate response using the agriculture bot
        bot_response = agri_bot.get_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for integration with existing websites"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        bot_response = agri_bot.get_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'timestamp': agri_bot.get_timestamp(),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Agriculture Chatbot'})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('chatbot', exist_ok=True)
    
    print("Agriculture Chatbot Starting...")
    print("Access at: http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/chat")
    
    app.run(debug=True, host='0.0.0.0', port=5000)