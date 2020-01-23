import unittest
import shutil
from pathlib import Path
from coarij.storage import Storage


class TestLedger(unittest.TestCase):
    ROOT = "ldata"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(Path.cwd().joinpath(cls.ROOT))

    def test_collect(self):
        storage = Storage(self.ROOT)
        path = storage.download(kind="XF", year=2018)
        ledger = storage.get_ledger(directory=f"{self.ROOT}/processed")
        self.assertGreater(len(ledger.data), 1)
        self.assertTrue(Path(ledger.path).exists)

        loaded = ledger.collect(edinet_code="E00021")
        self.assertGreater(len(loaded), 0)

    def test_collect_latest(self):
        storage = Storage(self.ROOT)
        path = storage.download(kind="XF", year=2018)
        ledger = storage.get_ledger(directory=f"{self.ROOT}/processed", latest=True)
        self.assertGreater(len(ledger.data), 1)
        self.assertTrue(Path(ledger.path).exists)

        loaded = ledger.collect(edinet_code="E00021")
        self.assertGreater(len(loaded), 0)

    def test_collect_csr(self):
        storage = Storage(self.ROOT)
        path = storage.download(kind="XF", year=2018)
        ledger = storage.get_ledger(directory=f"{self.ROOT}/processed")
        self.assertGreater(len(ledger.data), 1)
        self.assertTrue(Path(ledger.path).exists)

        loaded = ledger.collect(edinet_code="E00011", file_type="csr")
        self.assertGreater(len(loaded), 0)
