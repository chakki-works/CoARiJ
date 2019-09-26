from pathlib import Path
from datetime import datetime
from zipfile import ZipFile
import requests
import pandas as pd
from tqdm import tqdm
import edinet


class Storage():

    def __init__(self, root=""):
        _root = root if root else "data"
        self._default_raw_data = f"{_root}/raw"
        self._default_interim_data = f"{_root}/interim"
        self._default_processed_data = f"{_root}/processed"

    def download(self, directory="", kind="F", year="", force=False):
        DOWNLAD_URL = "https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial{}_{}.zip"  # noqa

        _kind = kind if len(kind) == 1 else kind[-1]
        default = self._default_interim_data if _kind == "E"\
                  else self._default_raw_data  # noqa
        dirname = directory if directory else default
        _directory = Path(dirname)
        if not _directory.is_absolute():
            _directory = Path.cwd().joinpath(dirname)

        year = str(year if year else datetime.now().year - 1)
        if _kind == "F":
            url = DOWNLAD_URL.format("", year)
        elif _kind == "E":
            url = DOWNLAD_URL.format("_extracted", year)
        else:
            raise Exception(f"Specified kind {kind} does not appropriate.")

        if len(kind) == 2 and kind[0] == "X":
            name_suffix = "_extracted" if _kind == "E" else ""
            url = DOWNLAD_URL.format(name_suffix, "example")

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
              source_directory="", target_directory="",
              year="", edinet_code="", sec_code="", jcn="",
              normalized=True):

        if not source_directory:
            s_dir = Path.cwd().joinpath(self._default_raw_data)
        else:
            s_dir = Path(source_directory)
            if not s_dir.is_absolute():
                s_dir = Path.cwd().joinpath(source_directory)

        if not target_directory:
            t_dir = Path.cwd().joinpath(self._default_interim_data)
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
        sec_code = str(sec_code)
        filters = {
            "edinet_code": edinet_code,
            "sec_code": sec_code + "0" if len(sec_code) == 4 else sec_code,
            "jcn": str(jcn)
            }
        for y in years:
            s_y_dir = s_dir.joinpath(y)
            documents = pd.read_csv(s_y_dir.joinpath("documents.csv"),
                                    sep="\t",  header=0)
            documents["sec_code"] = documents["sec_code"].astype(str)
            documents["jcn"] = documents["jcn"].astype(str)

            for k in filters:
                if filters[k]:
                    documents = documents[documents[k] == filters[k]]

            t_y_dir = t_dir.joinpath(y)
            t_y_dir.mkdir(parents=True, exist_ok=True)
            with t_y_dir.joinpath("documents.csv").open(
                    mode="w", encoding="utf-8") as f:
                documents.to_csv(f, header=True, index=False, sep="\t")

            t_y_dir = t_y_dir.joinpath("docs")
            t_y_dir.mkdir(exist_ok=True)
            print(f"Fiscal year {y}")
            total = len(documents)
            for i, doc_id in tqdm(iterable=documents["doc_id"].iteritems(),
                                  total=total):
                f = s_y_dir.joinpath(f"docs/{doc_id}.xbrl")
                try:
                    text = edinet.parse(f.absolute(), aspect, element)
                except Exception as ex:
                    print(f"Failed to parse {f.name} of {aspect_dot_element}.")

                base_name = aspect_dot_element.replace(".", "_")
                if normalized:
                    path = t_y_dir.joinpath(f"{f.stem}_{base_name}.txt")
                    with path.open("w", encoding="utf-8") as f:
                        f.write(text.value)
                else:
                    path = t_y_dir.joinpath(f"{f.stem}_{base_name}.html")
                    with path.open("w", encoding="utf-8") as f:
                        f.write(text.ground)

        return t_dir

    def tokenize(self, tokenizer="janome",
                 source_directory="", target_directory="",
                 year="", edinet_code="", sec_code="", jcn="",
                 aspect_dot_element="",
                 mode="", dictionary="", dictionary_type=""):

        tokenize = None

        if tokenizer == "janome":
            from janome.tokenizer import Tokenizer

            if not dictionary:
                _tokenizer = Tokenizer(wakati=True)
            else:
                _tokenizer = Tokenizer(dictionary, udic_type=dictionary_type,
                                       udic_enc="utf8", wakati=True)

            def tokenize(text):
                return _tokenizer.tokenize(text)

        elif tokenizer == "sudachi":
            from sudachipy.tokenizer import Tokenizer
            from sudachipy.dictionary import Dictionary

            if mode == "A":
                mode = Tokenizer.SplitMode.A
            elif mode == "B":
                mode = Tokenizer.SplitMode.B
            elif mode == "C":
                mode = Tokenizer.SplitMode.C

            _tokenizer = Dictionary().create()

            def tokenize(text):
                return [m.surface() for m in
                        _tokenizer.tokenize(text, mode)]

        else:
            raise Exception(f"Tokenizer {tokenizer} does not supported.")

        if not source_directory:
            s_dir = Path.cwd().joinpath(self._default_interim_data)
        else:
            s_dir = Path(source_directory)
            if not s_dir.is_absolute():
                s_dir = Path.cwd().joinpath(source_directory)

        if not target_directory:
            t_dir = Path.cwd().joinpath(self._default_processed_data)
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

        aspect_element = aspect_dot_element.replace(".", "_")
        sec_code = str(sec_code)
        filters = {
            "edinet_code": edinet_code,
            "sec_code": sec_code + "0" if len(sec_code) == 4 else sec_code,
            "jcn": str(jcn)
            }
        suffix = "_" + aspect_element if aspect_element else "*"
        for y in years:
            s_y_dir = s_dir.joinpath(y)
            documents = pd.read_csv(s_y_dir.joinpath("documents.csv"),
                                    sep="\t",  header=0)
            documents["sec_code"] = documents["sec_code"].astype(str)
            documents["jcn"] = documents["jcn"].astype(str)
            for k in filters:
                if filters[k]:
                    documents = documents[documents[k] == filters[k]]

            t_y_dir = t_dir.joinpath(y)
            t_y_dir.mkdir(parents=True, exist_ok=True)
            with t_y_dir.joinpath("documents.csv").open(
                    mode="w", encoding="utf-8") as f:
                documents.to_csv(f, header=True, index=False, sep="\t")

            t_y_dir = t_y_dir.joinpath("docs")
            t_y_dir.mkdir(exist_ok=True)
            total = len(documents)
            for i, doc_id in tqdm(iterable=documents["doc_id"].iteritems(),
                                  total=total):
                for f in s_y_dir.joinpath("docs").glob(f"{doc_id}{suffix}.txt"):
                    tokens = []
                    with f.open(encoding="utf-8") as fobj:
                        lines = fobj.readlines()
                        lines = [ln.strip() for ln in lines]
                        lines = [ln for ln in lines if ln]
                        tokens = [tokenize(ln) for ln in lines]

                    path = t_y_dir.joinpath(f"{f.stem}_tokenized.txt")
                    with path.open("w", encoding="utf-8") as f:
                        for ts in tokens:
                            f.write("\t".join(ts) + "\n")

        return t_dir
