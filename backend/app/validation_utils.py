import flask
from typing import Optional
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = {'.html', 'txt', 'docx', '.jpeg', '.jpg', '.png'}

def validate_upload(request: 'flask.Request') -> Optional[FileStorage]:
    """Validates uploaded file from request."""
    if 'file' not in request.files:
        return None

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return None
    
    if not uploaded_file.filename.endswith(tuple(ALLOWED_EXTENSIONS)):
        return None

    return uploaded_file
