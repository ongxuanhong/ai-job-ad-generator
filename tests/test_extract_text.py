import unittest
import json
import os
import tempfile
from scripts import extract_text


class TestExtractTextFromPDF(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        # Use a known small PDF file (or create one) for testing.
        sample_pdf = "data/documents/Software Engineer Position.pdf"
        sample_pdf = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), sample_pdf
        )
        result = extract_text.extract_text_from_pdf(sample_pdf)

        # Verify the result is a dict containing a list of paragraphs.
        self.assertIsInstance(result, dict)
        self.assertIn("paragraphs", result)
        self.assertIsInstance(result["paragraphs"], list)
        self.assertGreater(
            len(result["paragraphs"]), 0, "No paragraphs extracted from the PDF."
        )

        # Test saving to JSON using a temporary directory.
        with tempfile.TemporaryDirectory() as tmpdirname:
            out_file = os.path.join(tmpdirname, "out.json")
            extract_text.save_text_to_json(result, out_file)

            # Load back the JSON to verify it was written correctly.
            with open(out_file, "r") as f:
                loaded = json.load(f)
            self.assertEqual(loaded, result)


if __name__ == "__main__":
    unittest.main()
