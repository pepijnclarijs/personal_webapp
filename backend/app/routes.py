import os
from flask import Blueprint, request, jsonify
from backend.app.utils import save_file

# Create a blueprint to handle the routes
main = Blueprint('main', __name__)

# Define the route for file upload and PDF conversion
@main.route('/convert', methods=['POST'])
def convert_to_pdf():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Define the upload folder path
    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')

    # Save the file using the utility function
    try:
        file_path = save_file(file, upload_folder)
        return jsonify({"message": "File uploaded successfully!", "file_path": file_path}), 200
    except Exception as e:
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500
