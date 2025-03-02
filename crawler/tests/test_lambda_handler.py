import sys
import os
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
  
import json
from crawler.lambda_handler import lambda_handler  # Now this should work

def test_crawler_lambda():
    event = {}  # Adjust event data as needed
    result = lambda_handler(event, None)
    print("Crawler Lambda Response:")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    test_crawler_lambda()
