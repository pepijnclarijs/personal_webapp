# Integration tests to test the routes.

import unittest
from pathlib import Path
from backend.app import create_app
from docx import Document


class TestFileUploadAndConversion(unittest.TestCase):

    def setUp(self):
        """Set up test client and other test-specific configurations."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.upload_folder = Path("test_uploads")
        self.upload_folder.mkdir(exist_ok=True)  # Create the upload folder if it doesn't exist
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder

        # Create sample upload files
        self.docx_file_path = self.upload_folder / "sample.docx"
        self.txt_file_path = self.upload_folder / "sample.txt"
        self.unsupported_file_path = self.upload_folder / "unsupported.exe"
        self.create_sample_files()

    def tearDown(self):
        """Clean up files after tests."""
        for file_path in self.upload_folder.iterdir():
            file_path.unlink()  # Remove each file
        self.upload_folder.rmdir()  # Remove the directory

    def test_upload_and_convert_txt_file(self):
        """Test uploading and converting a .txt file to PDF."""
        with self.txt_file_path.open('rb') as f:  # Open the sample text file as binary
            data = {'file': (f, self.txt_file_path.name)}
            response = self.client.post('/convert', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File converted successfully!', response.data)

    def test_upload_and_convert_docx_file(self):
        """Test uploading and converting a .docx file to PDF."""
        with self.docx_file_path.open('rb') as f:  # Open the sample docx file as binary
            data = {'file': (f, self.docx_file_path.name)}
            response = self.client.post('/convert', content_type='multipart/form-data', data=data)
            # If the response status code is not 200, fail the test with the response data.
            if response.status_code != 200:
                self.fail(f"Expected status code 200, but got {response.status_code}. "
                        f"Response content: {response.data.decode()}")
            self.assertIn(b'File converted successfully!', response.data)

    def test_upload_and_convert_unsupported_file(self):
        """Test uploading unsupported file types and receiving an error."""
        with self.unsupported_file_path.open('rb') as f:  # Open the unsupported file as binary
            data = {'file': (f, self.unsupported_file_path.name)}
            response = self.client.post('/convert', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Invalid file upload.', response.data)

    def create_sample_docx_file(self):
        """Create a sample.docx file."""
        doc = Document()
        doc.add_paragraph("Sample DOCX content.")
        doc.save(self.docx_file_path)

    def create_sample_txt_file(self):
        """Create a sample.txt file."""
        txt_file_path = self.upload_folder / "sample.txt"
        with txt_file_path.open('w') as f:
            f.write("Sample text content")

    def create_sample_unsupported_file(self):
        """Create a sample unsupported file (e.g., .exe)."""
        unsupported_file_path = self.upload_folder / "unsupported.exe"
        with unsupported_file_path.open('wb') as f:
            f.write(b'Some content')

    def create_sample_files(self):
        """Create all sample files needed for tests."""
        self.create_sample_docx_file()
        self.create_sample_txt_file()
        self.create_sample_unsupported_file()
