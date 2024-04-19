# Local test script to test the handler function with a sample event.
from datetime import datetime
import json
import unittest

import os
import sys

PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH)

from entry import handler

class TestHandler(unittest.TestCase):
  def test_handler(self):
    with open("./test/event.json", "r") as f:
      event = json.load(f)
      event["Username"] = f"Tester-{datetime.timestamp(datetime.now())}"

    response = handler(event, None)
    self.assertIsNotNone(response, msg="Received None response")
    self.assertIsInstance(response, dict, msg="Response is not a dictionary")
    self.assertIn("data", response, msg="Response does not contain 'data' key")
    self.assertIn("ResponseMetadata", response.get("data"), msg="Response does not contain 'ResponseMetadata' key")
    self.assertEqual(response["data"]["ResponseMetadata"].get("HTTPStatusCode"), 200, msg="Status Code not ok")
    
  def test_bad_event(self):
    response = handler({}, None)
    self.assertIsNotNone(response)
    self.assertIsInstance(response, dict)
    self.assertIn("error", response)

if __name__ == "__main__":
  os.environ["TEST"] = "True"
  unittest.main()
