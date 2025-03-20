import os
import unittest
from unittest.mock import patch, MagicMock, ANY
from scripts.generate_visual import create_job_ad_visual


class TestGenerateVisual(unittest.TestCase):
    @patch("scripts.generate_visual.requests.get")
    @patch("scripts.generate_visual.fal_client.subscribe")
    def test_create_job_ad_visual(self, mock_subscribe, mock_get):
        # Setup fake API result simulating the pre-generated image JSON
        fake_api_result = {
            "images": [
                {
                    "url": "https://v3.fal.media/files/lion/D3Hx5EJFraEd6sTCjp0UG_image.webp",
                    "file_name": "image.webp",
                    "file_size": 280156,
                    "content_type": "image/webp",
                }
            ]
        }
        mock_subscribe.return_value = fake_api_result

        # Setup a fake image response with sample binary content
        fake_image_content = b"fake_image_data"
        fake_response = MagicMock()
        fake_response.content = fake_image_content
        fake_response.raise_for_status.return_value = None
        mock_get.return_value = fake_response

        title = "Senior Data Analyst"
        summary = (
            "- Develop high-quality software solutions using modern web technologies.\n"
            "- Collaborate with cross-functional teams to design, develop, and deliver scalable applications.\n"
            "- Maintain code integrity and organization."
        )

        # Call the function to generate the visual
        image_path = create_job_ad_visual(title, summary)

        # Check that the file name ends with '.webp'
        self.assertTrue(image_path.endswith(".webp"))

        # Verify the file was written and its content matches the fake image data
        with open(image_path, "rb") as f:
            saved_content = f.read()
        self.assertEqual(saved_content, fake_image_content)

        # Optionally, assert that fal_client.subscribe was called with expected parameters
        mock_subscribe.assert_called_once_with(
            "fal-ai/recraft-v3",
            arguments={
                "prompt": ANY,  # The prompt is constructed dynamically
                "image_size": "square_hd",
                "style": "realistic_image",
                "colors": [],
            },
            with_logs=True,
            on_queue_update=ANY,
        )

        # Clean up the created file
        os.remove(image_path)


if __name__ == "__main__":
    unittest.main()
