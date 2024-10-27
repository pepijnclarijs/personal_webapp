import os
import pypandoc
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .routes import main


# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Set configuration from .env file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    CORS(app)  # Enable CORS to allow cross-origin requests from frontend

    app.register_blueprint(main)

    return app
