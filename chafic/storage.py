from pathlib import Path
from datetime import datetime
from zipfile import ZipFile
import requests
from tqdm import tqdm


class Storage():

    def __init__(self):
        pass

    def download(self, directory="", year="", kind="R", force=False):
        DOWNLAD_URL = "https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial{}_{}.zip"  # noqa

        directory = Path(directory) if directory else Path.cwd()
        if not directory.is_absolute():
            directory = Path.cwd().joinpath(directory)

        year = year if year else datetime.now().year - 1

        if kind == "R":
            url = DOWNLAD_URL.format("", year)
        elif kind == "E":
            url = DOWNLAD_URL.format("_extracted", year)
        elif len(kind) == 2 and kind[0] == "X":
            _kind = "_extracted" if kind[1] == "E" else ""
            url = DOWNLAD_URL.format(_kind, "example")
        else:
            raise Exception(f"Specified kind {kind} does not appropriate.")

        if not directory.exists():
            directory.mkdir()
        file_name = url.split("/")[-1]
        path = directory.joinpath(file_name)

        if path.exists() and not force:
            print(f"Download file {file_name} is already exist.")
            return path
        elif directory.joinpath(year).exists() and not force:
            print(f"Expanded directory {year} is already exist.")
            return directory.joinpath(year)

        resp = requests.get(url, stream=True)
        if not resp.ok:
            raise Exception("Can not get dataset from {}.".format(url))

        total_size = int(resp.headers.get("content-length", 0))
        print(f"Download {file_name}")
        with path.open(mode="wb") as f:
            chunk_size = 1024
            limit = total_size / chunk_size
            for data in tqdm(resp.iter_content(chunk_size=chunk_size),
                             total=limit, unit="B", unit_scale=True):
                f.write(data)

        print(f"Expand {file_name}")
        with ZipFile(path) as zip:
            for f in tqdm(iterable=zip.namelist(), total=len(zip.namelist())):
                zip.extract(member=f, path=directory)

        path.unlink()

        return directory.joinpath(year)
