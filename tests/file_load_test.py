import json
import os
import tempfile
import unittest
from unittest.mock import patch
from firefox_bookmarks_deduplicator import file_operations


def open_with_legacy_encoding(*args, **kwargs):
    kwargs.setdefault("encoding", "cp1252")
    return open(*args, **kwargs)


class FileLoadTestSuite(unittest.TestCase):

    def test_file_load(self):
        bookmarks_object = file_operations.load_bookmarks_file("tests/testcase1.json")
        self.assertEqual(bookmarks_object.get("root"), "placesRoot")
        self.assertEqual(len(bookmarks_object.get("children")), 3)

    def test_file_load_uses_utf8_with_legacy_system_encoding(self):
        expected = {"title": "Caf\u00e9 \u65e5\u672c\u8a9e"}
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "bookmarks.json")
            with open(filename, "w", encoding="utf-8") as output:
                json.dump(expected, output, ensure_ascii=False)

            with patch.object(file_operations, "open", open_with_legacy_encoding, create=True):
                bookmarks_object = file_operations.load_bookmarks_file(filename)

        self.assertEqual(bookmarks_object, expected)

    def test_file_write_uses_utf8_with_legacy_system_encoding(self):
        output = json.dumps({"title": "Caf\u00e9 \u65e5\u672c\u8a9e"}, ensure_ascii=False)
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "bookmarks.json")
            with patch.object(file_operations, "open", open_with_legacy_encoding, create=True):
                file_operations.write_to_file(filename, output)

            with open(filename, "rb") as bookmarks_file:
                self.assertEqual(bookmarks_file.read(), output.encode("utf-8"))


if __name__ == '__main__':
    unittest.main() 
