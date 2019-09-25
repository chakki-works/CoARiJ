import unittest
import shutil
import os
from pathlib import Path
from chafic.storage import Storage


class TestStorage(unittest.TestCase):

    def test_download_raw(self):
        storage = Storage()
        path = storage.download(directory="data/", kind="XR", year=2018)
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")
        shutil.rmtree(Path.cwd().joinpath("data"))

    def test_download_extracted(self):
        storage = Storage()
        path = storage.download(directory="data_extracted/", kind="XE", year=2018)
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")
        shutil.rmtree(Path.cwd().joinpath("data_extracted"))
