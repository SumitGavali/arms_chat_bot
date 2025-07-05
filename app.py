from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_chatbot_response
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('base.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot responses"""
    try:
        # Get user message from request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'response': 'Please send a message.'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'response': 'Please send a valid message.'
            }), 400
        
        # Log the user message
        logger.info(f"User message: {user_message}")
        
        # Get chatbot response
        bot_response = get_chatbot_response(user_message)
        
        # Log the bot response
        logger.info(f"Bot response: {bot_response}")
        
        return jsonify({
            'response': bot_response,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'response': 'Sorry, something went wrong. Please try again.'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'Chatbot service is running'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource was not found.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end.'
    }), 500

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # For production, use:
    # app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
