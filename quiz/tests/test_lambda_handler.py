import json
import os
import tempfile
import unittest
from quiz.lambda_handler import lambda_handler
from common.config import USE_AWS

class TestQuizLambdaHandler(unittest.TestCase):
    def test_lambda_handler_local(self):
        # In AWS mode, this test may not run correctly without valid S3 data.
        if USE_AWS:
            self.skipTest("Skipping local test because USE_AWS is set to True.")
        
        # Create a temporary file with sample intermediate content.
        sample_intermediate_content = "This is sample crawled content for quiz testing."
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write(sample_intermediate_content)
            temp_file_path = temp_file.name

        # Prepare event using the temporary file path as the 's3_key'
        event = {
            "website_url": "https://www.example.com",
            "s3_key": temp_file_path
        }
        
        result = lambda_handler(event, None)
        print("Quiz Lambda Response:")
        print(json.dumps(result, indent=4))
        
        # Optionally, assert that the status code is 200.
        self.assertEqual(result.get("statusCode"), 200)
        
        # Cleanup temporary file.
        os.remove(temp_file_path)

if __name__ == "__main__":
    unittest.main()
