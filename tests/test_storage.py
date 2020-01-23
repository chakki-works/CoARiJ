import unittest
import shutil
from pathlib import Path
from coarij.storage import Storage


class TestStorage(unittest.TestCase):
    ROOT = "tdata"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(Path.cwd().joinpath(cls.ROOT))

    def test_download(self):
        path = self._download()
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")
        self.assertTrue(path.joinpath("documents.csv").exists())
        self.assertTrue(path.joinpath("docs").exists())
        self.assertGreater(
            len(list(path.joinpath("docs").glob("*.xbrl"))), 1)

    def test_download_ledger(self):
        storage = Storage(self.ROOT)
        ledger = storage.get_ledger(directory=f"{self.ROOT}/processed")
        self.assertGreater(len(ledger.data), 1)
        self.assertTrue(Path(ledger.path).exists)

    def test_download_extracted(self):
        storage = Storage(self.ROOT)
        path = storage.download(directory=f"{self.ROOT}/rawe", kind="XE", year=2018)
        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2018")
        self.assertTrue(path.joinpath("documents.csv").exists())
        self.assertTrue(path.joinpath("docs").exists())
        self.assertGreater(
            len(list(path.joinpath("docs").glob("*.txt"))), 1)

    def test_parse(self):
        storage = Storage(self.ROOT)
        path = self._download(kind="F")
        path = storage.extract("company.history")
        self.assertTrue(path.exists())
        self.assertTrue(path.joinpath("2018").exists())
        self.assertTrue(path.joinpath("2018/documents.csv").exists())
        self.assertGreater(
            len(list(path.joinpath("2018/docs").glob("*company_history.txt"))), 0)

        path = storage.extract("business.risks", sec_code="1376")
        with path.joinpath("2018/documents.csv").open(encoding="utf-8") as f:
            self.assertEquals(len(f.readlines()), 2)
        self.assertEquals(
            len(list(path.joinpath("2018/docs").glob("*business_risks.txt"))), 1)

    def test_tokenize(self):
        storage = Storage(self.ROOT)
        path = self._download(kind="F")
        path = storage.extract("company.history")
        path = storage.tokenize(tokenizer="janome")
        self.assertTrue(path.exists())
        self.assertTrue(path.joinpath("2018").exists())
        self.assertTrue(path.joinpath("2018/documents.csv").exists())
        self.assertGreater(
            len(list(path.joinpath("2018/docs").glob(
                "*company_history_tokenized.txt"))), 0)

        path = storage.extract("business.risks", sec_code="1376")
        path = storage.tokenize(tokenizer="sudachi")
        with path.joinpath("2018/documents.csv").open(encoding="utf-8") as f:
            self.assertEquals(len(f.readlines()), 2)
        self.assertEquals(
            len(list(path.joinpath("2018/docs").glob(
                "*business_risks_tokenized.txt"))), 1)

    def _download(self, kind="F"):
        storage = Storage(self.ROOT)
        path = storage.download(kind="X" + kind, year=2018)
        return path
