# Define the route for file upload and PDF conversion
import tempfile
from flask import Blueprint, request, jsonify
from backend.app.conversion_utils import handle_pdf_conversion
from backend.app.file_utils import save_file
from backend.app.validation_utils import validate_upload

# Create a blueprint to handle the routes
main = Blueprint('main', __name__)

@main.route('/convert', methods=['POST'])
def convert_to_pdf():
    """Converts uploaded files to PDF."""
    uploaded_file = validate_upload(request)
    if uploaded_file is None:
        return jsonify({"error": "Invalid file upload."}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        uploaded_file_path = save_file(uploaded_file, temp_dir)
        if uploaded_file_path is None:
            return jsonify({"error": "File upload failed."}), 500
        
        return handle_pdf_conversion(uploaded_file_path)
