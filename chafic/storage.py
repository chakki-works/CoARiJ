from pathlib import Path
from datetime import datetime
from zipfile import ZipFile
import requests
from tqdm import tqdm
import edinet


class Storage():

    def __init__(self, root=""):
        _root = root if root else "data"
        self._default_raw_data = f"{_root}/raw"
        self._default_processed_data = f"{_root}/processed"

    def _kind_to_path(self, kind):
        k = kind if len(kind) == 1 else kind[-1]
        if k == "F":
            return "files"
        elif k == "E":
            return "extracteds"
        else:
            return ""

    def download(self, directory="", kind="F", year="", force=False):
        DOWNLAD_URL = "https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial{}_{}.zip"  # noqa

        dirname = directory if directory else self._default_raw_data
        _directory = Path(dirname)
        if not _directory.is_absolute():
            _directory = Path.cwd().joinpath(dirname)

        year = str(year if year else datetime.now().year - 1)

        if kind == "F":
            url = DOWNLAD_URL.format("", year)
        elif kind == "E":
            url = DOWNLAD_URL.format("_extracted", year)
        elif len(kind) == 2 and kind[0] == "X":
            _kind = "_extracted" if kind[1] == "E" else ""
            url = DOWNLAD_URL.format(_kind, "example")
        else:
            raise Exception(f"Specified kind {kind} does not appropriate.")

        _directory = _directory.joinpath(self._kind_to_path(kind))
        if not _directory.exists():
            _directory.mkdir(parents=True, exist_ok=True)
        file_name = url.split("/")[-1]
        path = _directory.joinpath(file_name)

        if path.exists() and not force:
            print(f"Download file {file_name} is already exist.")
            return path
        elif _directory.joinpath(year).exists() and not force:
            print(f"Expanded directory {year} is already exist.")
            return _directory.joinpath(year)

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
                zip.extract(member=f, path=_directory)

        path.unlink()

        return _directory.joinpath(year)

    def parse(self, aspect_dot_element,
              source_directory="", target_directory="", year="",
              normalized=True):

        if not source_directory:
            s_dir = Path.cwd().joinpath(self._default_raw_data)
            s_dir = s_dir.joinpath(self._kind_to_path("F"))
        else:
            s_dir = Path(source_directory)
            if not s_dir.is_absolute():
                s_dir = Path.cwd().joinpath(source_directory)

        if not target_directory:
            t_dir = Path.cwd().joinpath(self._default_processed_data)
            t_dir = t_dir.joinpath(self._kind_to_path("F"))
        else:
            t_dir = Path(target_directory)
            if not t_dir.is_absolute():
                t_dir = Path.cwd().joinpath(target_directory)

        if not s_dir.exists():
            raise Exception(f"Files does not exist at {s_dir}")

        years = [year] if year else []
        if len(years) == 0:
            for d in s_dir.iterdir():
                if d.is_dir():
                    years.append(d.name)

        aspect, element = aspect_dot_element.split(".")
        for y in years:
            y_dir = s_dir.joinpath(y).joinpath("docs")
            t_dir = t_dir.joinpath(y)
            t_dir.mkdir(parents=True, exist_ok=True)

            for f in y_dir.glob("*.xbrl"):
                try:
                    text = edinet.parse(f.absolute(), aspect, element)
                except Exception as ex:
                    print(f"Failed to parse {f.name} of {aspect_dot_element}.")

                base_name = aspect_dot_element.replace(".", "_")
                if normalized:
                    path = t_dir.joinpath(f"{f.stem}_{base_name}.txt")
                    with path.open("w", encoding="utf-8") as f:
                        f.write(text.value)
                else:
                    path = t_dir.joinpath(f"{f.stem}_{base_name}.html")
                    with path.open("w", encoding="utf-8") as f:
                        f.write(text.ground)

        return t_dir
