import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))
os.environ["TABLE_NAME"] = "test-intake"
os.environ["APP_VERSION"] = "v1"

import handler


class FakeTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):
        self.items.append(Item)


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.table = FakeTable()
        handler._table = self.table

    def test_writes_metadata(self):
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": "demo"},
                        "object": {"key": "uploads/photo.jpg", "size": 42},
                    }
                }
            ]
        }
        # head_object may try boto3; force the except path by making import work but client fail
        fake_boto = mock.MagicMock()
        fake_boto.client.side_effect = RuntimeError("no aws")
        with mock.patch.dict(sys.modules, {"boto3": fake_boto}):
            res = handler.lambda_handler(event, None)
        self.assertTrue(res["ok"])
        self.assertEqual(len(self.table.items), 1)
        self.assertEqual(self.table.items[0]["object_key"], "uploads/photo.jpg")
        self.assertEqual(self.table.items[0]["size"], 42)
        self.assertEqual(self.table.items[0]["version"], "v1")

    def test_skips_non_uploads(self):
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": "demo"},
                        "object": {"key": "other/file.bin", "size": 1},
                    }
                }
            ]
        }
        handler.lambda_handler(event, None)
        self.assertEqual(self.table.items, [])


if __name__ == "__main__":
    unittest.main()
