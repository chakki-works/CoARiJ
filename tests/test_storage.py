import unittest
import shutil
from pathlib import Path
from chafic.storage import Storage


class TestStorage(unittest.TestCase):
    ROOT = "tdata"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(Path.cwd().joinpath("tdata"))

    def test_download_raw_then_parse(self):
        storage = Storage(self.ROOT)
        path = storage.download(kind="XF", year=2018)
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")

        path = storage.parse("company.history")
        self.assertTrue(path.exists())
        self.assertGreater(len(list(path.glob("*.txt"))), 0)

    def test_download_extracted(self):
        storage = Storage(self.ROOT)
        path = storage.download(kind="XE", year=2018)
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")
