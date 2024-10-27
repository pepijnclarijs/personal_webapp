# Unittests for the conversion_utils module

from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock, mock_open
from backend.app import create_app  # Adjust the import according to your app structure
from backend.app.conversion_utils import (
    convert_txt_to_pdf,
    convert_docx_to_pdf,
    convert_image_to_pdf,
    handle_pdf_conversion
)

class TestFileConversions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Create your Flask app instance
        cls.app_context = cls.app.app_context()  # Create app context

    def setUp(self):
        self.app_context.push()  # Push the app context before each test

    def tearDown(self):
        self.app_context.pop()  # Pop the app context after each test

    @patch('pdfkit.from_string')  # Mock pdfkit for txt to pdf conversion
    def test_convert_txt_to_pdf(self, mock_pdfkit):
        mock_pdfkit.return_value = None  # Simulate successful conversion
        txt_file = 'test.txt'
        output_pdf = 'output.pdf'
        
        with patch('builtins.open', mock_open(read_data='Sample text for testing.')):
            convert_txt_to_pdf(txt_file, output_pdf)
        
        mock_pdfkit.assert_called_once_with('<pre>Sample text for testing.</pre>', output_pdf)

    @patch('pypandoc.convert_file')  # Mock pypandoc for docx to pdf conversion
    def test_convert_docx_to_pdf(self, mock_pypandoc):
        mock_pypandoc.return_value = None  # Simulate successful conversion
        docx_file = 'test.docx'
        output_pdf = 'output.pdf'
        
        convert_docx_to_pdf(docx_file, output_pdf)
        
        mock_pypandoc.assert_called_once_with(docx_file, 'pdf', outputfile=output_pdf)

    @patch('PIL.Image.open')  # Mock Pillow for image to pdf conversion
    def test_convert_image_to_pdf(self, mock_open):
        mock_image = MagicMock()  # Create a mock image object with a save method
        mock_open.return_value = mock_image  # Return the mocked image when opened
        output_pdf = 'output.pdf'
        
        convert_image_to_pdf('test_image.png', output_pdf)
        
        mock_open.assert_called_once_with('test_image.png')  # Verify Image.open was called
        mock_image.save.assert_called_once_with(output_pdf, 'PDF')  # Verify save was called

    @patch('backend.app.conversion_utils.change_extension_to_pdf')
    @patch('backend.app.conversion_utils.convert_txt_to_pdf')
    def test_handle_pdf_conversion_txt(self, mock_convert_txt_to_pdf, mock_change_extension_to_pdf):
        # Setup mock behavior
        mock_change_extension_to_pdf.return_value = "test.pdf"  # Expected output path

        # Call the function with a .txt file
        response = handle_pdf_conversion("test.txt")

        # Assertions
        mock_change_extension_to_pdf.assert_called_once_with(Path("test.txt"))
        mock_convert_txt_to_pdf.assert_called_once_with(Path("test.txt"), Path("test.pdf"))
        self.assertEqual(response[1], 200)

    @patch('backend.app.conversion_utils.change_extension_to_pdf', return_value='test.pdf')
    @patch('backend.app.conversion_utils.convert_docx_to_pdf')
    def test_handle_pdf_conversion_docx(self, mock_convert_docx, mock_change_extension_to_pdf):
        # Call the function with a .docx file
        response = handle_pdf_conversion('test.docx')
        
        # Assertions
        mock_change_extension_to_pdf.assert_called_once_with(Path('test.docx'))
        mock_convert_docx.assert_called_once_with(Path('test.docx'), Path('test.pdf'))
        self.assertEqual(response[1], 200)

    @patch('backend.app.conversion_utils.change_extension_to_pdf', return_value='test_image.pdf')
    @patch('backend.app.conversion_utils.convert_image_to_pdf')
    def test_handle_pdf_conversion_image(self, mock_convert_image, mock_change_extension_to_pdf):
        response = handle_pdf_conversion('test_image.png')
        
        mock_change_extension_to_pdf.assert_called_once_with(Path('test_image.png'))  # Ensure correct output path
        mock_convert_image.assert_called_once_with(Path('test_image.png'), Path('test_image.pdf'))  # Ensure correct conversion function called
        self.assertEqual(response[1], 200)

    @patch('backend.app.conversion_utils.change_extension_to_pdf', return_value='test.pdf')
    def test_handle_pdf_conversion_unsupported_type(self, mock_change_extension_to_pdf):
        response = handle_pdf_conversion('test.exe')
        
        mock_change_extension_to_pdf.assert_called_once_with(Path('test.exe'))  # Ensure correct output path
        self.assertIn("File type .exe not supported.", response[0].get_data(as_text=True))
        self.assertEqual(response[1], 400)


if __name__ == '__main__':
    unittest.main()
