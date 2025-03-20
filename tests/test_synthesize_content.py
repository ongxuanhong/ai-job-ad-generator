import os
import json
import tempfile
import unittest
from scripts.synthesize_content import generate_job_ad_content, save_generated_content


class TestSynthesizeContent(unittest.TestCase):
    def setUp(self):
        # Ensure the API key is set before running tests that require an actual API call.
        if not os.getenv("OPENAI_API_KEY"):
            self.skipTest(
                "OPENAI_API_KEY is not set. Skipping tests that require OpenAI API."
            )

    def test_generate_job_ad_content(self):
        # Create a sample text_data dict with multiple paragraphs.
        text_data = {
            "paragraphs": [
                "We are seeking an experienced software engineer to join our team.",
                "The candidate will be responsible for developing scalable applications.",
                "Experience with Python, JavaScript, and cloud services is required.",
                "The role includes code reviews, design discussions, and agile development practices.",
                "Benefits include competitive salary, health insurance, and remote work options.",
                "Additional perks include professional development opportunities and team events.",
            ]
        }
        # This call makes an actual API request.
        result = generate_job_ad_content(text_data)

        # Check that the result is a dict containing the expected keys.
        self.assertIsInstance(result, dict)
        expected_keys = [
            "job_title",
            "summary",
            "responsibilities",
            "requirements",
            "qualifications",
        ]
        for key in expected_keys:
            self.assertIn(
                key, result, f"Key '{key}' not found in the generated content."
            )

    def test_save_generated_content(self):
        # Sample content to save.
        content = {
            "job_title": "Software Engineer",
            "summary": "Develop and maintain scalable software solutions.",
            "responsibilities": "Design, code, and collaborate with cross-functional teams.",
            "requirements": "Bachelor's degree in Computer Science or related field.",
            "qualifications": "Proficiency in Python and experience with cloud platforms.",
        }
        # Use a temporary file to test saving functionality.
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, suffix=".json"
        ) as tmp_file:
            tmp_file_path = tmp_file.name

        try:
            save_generated_content(content, tmp_file_path)
            # Read back the file to verify its content.
            with open(tmp_file_path, "r", encoding="utf-8") as f:
                loaded_content = json.load(f)
            self.assertEqual(
                content,
                loaded_content,
                "Saved content does not match the original content.",
            )
        finally:
            os.remove(tmp_file_path)


if __name__ == "__main__":
    unittest.main()
