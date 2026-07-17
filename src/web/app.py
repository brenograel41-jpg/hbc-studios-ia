"""
GHS STUDIOS IA - Web Interface
Flask application for web-based chat
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

from ..bot import ChatBot

logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # CORS
    CORS(app, resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', '*')}})
    
    # Initialize chatbot
    app.chatbot = ChatBot()
    
    # =====================================================================
    # Routes
    # =====================================================================
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html', version='1.0.0')
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }), 200
    
    @app.route('/api/models', methods=['GET'])
    def get_models():
        """Get available models"""
        models = {
            'free': [
                {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo', 'provider': 'OpenAI'},
                {'id': 'gemini', 'name': 'Google Gemini', 'provider': 'Google'},
            ],
            'paid': [
                {'id': 'gpt-4', 'name': 'GPT-4', 'provider': 'OpenAI'},
                {'id': 'claude-3-opus-20240229', 'name': 'Claude 3 Opus', 'provider': 'Anthropic'},
                {'id': 'command', 'name': 'Cohere Command', 'provider': 'Cohere'},
            ]
        }
        return jsonify(models), 200
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Send a message and get response"""
        try:
            data = request.get_json()
            
            if not data or 'message' not in data:
                return jsonify({'error': 'Message required'}), 400
            
            message = data.get('message', '').strip()
            if not message:
                return jsonify({'error': 'Message cannot be empty'}), 400
            
            if 'model' in data:
                app.chatbot.switch_model(data['model'])
            
            response = app.chatbot.chat(message)
            
            return jsonify({
                'success': True,
                'message': message,
                'response': response,
                'model': app.chatbot.model,
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/history', methods=['GET'])
    def get_history():
        """Get conversation history"""
        try:
            history = app.chatbot.get_history()
            return jsonify({
                'success': True,
                'history': history,
                'count': len(history)
            }), 200
        except Exception as e:
            logger.error(f"History error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/clear-history', methods=['POST'])
    def clear_history():
        """Clear conversation history"""
        try:
            app.chatbot.clear_history()
            return jsonify({
                'success': True,
                'message': 'History cleared'
            }), 200
        except Exception as e:
            logger.error(f"Clear history error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/export', methods=['POST'])
    def export():
        """Export conversation"""
        try:
            filename = app.chatbot.export_conversation()
            return jsonify({
                'success': True,
                'filename': filename,
                'message': 'Conversation exported'
            }), 200
        except Exception as e:
            logger.error(f"Export error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)