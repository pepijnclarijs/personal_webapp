# Integration test for the file_utils.py module.
import os
import random
import string
import unittest
from backend.app.file_utils import change_extension_to_pdf, get_unique_filename, save_file
from werkzeug.datastructures import FileStorage


def random_string(length=8):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class TestFileUtils(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a temporary upload folder for testing."""
        self.test_upload_folder = f"test_uploads_{random_string()}"
        if not os.path.exists(self.test_upload_folder):
            os.makedirs(self.test_upload_folder)

    def tearDown(self) -> None:
        """Clean up the test upload folder after tests."""
        for filename in os.listdir(self.test_upload_folder):
            file_path = os.path.join(self.test_upload_folder, filename)
            os.remove(file_path)
        os.rmdir(self.test_upload_folder)

    def test_get_unique_filename_creates_unique_name(self) -> None:
        """Test that get_unique_filename creates a unique name."""
        # Create a dummy file in the test folder
        existing_file_path = os.path.join(self.test_upload_folder, "test_file.txt")
        with open(existing_file_path, 'w') as f:
            f.write("Dummy content")

        # Now get a unique filename for the same base name
        new_file_path = get_unique_filename("test_file.txt", self.test_upload_folder)

        # Assert that the new file path is unique
        self.assertIn("(1)", os.path.basename(new_file_path))
        self.assertEqual(new_file_path, os.path.join(self.test_upload_folder, "test_file (1).txt"))

        # Clean up
        os.remove(existing_file_path)

    def test_save_file(self) -> None:
        """Test that save_file correctly saves a file."""
        # Create a file in the test folder to simulate an upload
        file_path = os.path.join(self.test_upload_folder, 'test_file.txt')
        with open(file_path, 'w+b') as temp_file:
            temp_file.write(b"Test content")  # Write some content to the file

        # Open the mock file from the test folder
        with open(file_path, 'rb') as mock_file_stream:
            mock_file = FileStorage(
                stream=mock_file_stream,
                filename='test_file.txt'
            )

            # Save the file using the save_file function
            saved_file_path = save_file(mock_file, self.test_upload_folder)

            # Assert that the file is saved correctly
            self.assertTrue(os.path.exists(saved_file_path))

        # Clean up
        os.remove(saved_file_path)


class TestChangeExtensionToPdf(unittest.TestCase):

    def test_change_txt_to_pdf(self):
        self.assertEqual(change_extension_to_pdf("hello.txt"), "hello.pdf")

    def test_change_md_to_pdf(self):
        self.assertEqual(change_extension_to_pdf("document.md"), "document.pdf")

    def test_change_no_extension_to_pdf(self):
        self.assertEqual(change_extension_to_pdf("file_without_extension"), "file_without_extension.pdf")

    def test_change_pdf_to_pdf(self):
        self.assertEqual(change_extension_to_pdf("already_a_pdf.pdf"), "already_a_pdf.pdf")

    def test_change_nested_file_path(self):
        self.assertEqual(change_extension_to_pdf("folder/subfolder/hello.txt"), "folder/subfolder/hello.pdf")

    def test_change_large_file_name(self):
        self.assertEqual(change_extension_to_pdf("very_long_file_name_with_multiple_words.txt"), "very_long_file_name_with_multiple_words.pdf")


if __name__ == "__main__":
    unittest.main()
