import unittest
import shutil
from chafic.storage import Storage


class TestStorage(unittest.TestCase):

    def test_download(self):
        storage = Storage()
        path = storage.download(directory="data/", kind="XR", year=2018)
        shutil.rmtree(path)
