from pathlib import Path
from datetime import datetime
from zipfile import ZipFile
import requests
import pandas as pd
from tqdm import tqdm
import xbrr
from coarij.ledger import Ledger


class Storage():

    def __init__(self, root=""):
        _root = root if root else "data"
        self._default_raw_data = f"{_root}/raw"
        self._default_interim_data = f"{_root}/interim"
        self._default_processed_data = f"{_root}/processed"

    def get_ledger(self, directory="", force=False, latest=False):
        url = "https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/coarij.csv"  # noqa
        if latest:
            url = "https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/coarij_latest.csv"  # noqa

        dirname = directory if directory else self._default_processed_data
        _directory = Path(dirname)
        if not _directory.is_absolute():
            _directory = Path.cwd().joinpath(dirname)

        if not _directory.exists():
            _directory.mkdir(parents=True, exist_ok=True)
        file_name = url.split("/")[-1]
        path = _directory.joinpath(file_name)

        if path.exists():
            return Ledger(self, path)

        resp = requests.get(url, stream=True)
        if not resp.ok:
            resp.raise_for_status()

        total_size = int(resp.headers.get("content-length", 0))
        print(f"Download coarij ledger.")
        with path.open(mode="wb") as f:
            chunk_size = 1024
            limit = total_size / chunk_size
            for data in tqdm(resp.iter_content(chunk_size=chunk_size),
                             total=limit, unit="B", unit_scale=True):
                f.write(data)

        ledger = Ledger(self, path)

        return ledger

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

        print(f"Download {file_name}")
        self._download(url, path)

        print(f"Expand {file_name}")
        with ZipFile(path) as zip:
            for f in tqdm(iterable=zip.namelist(), total=len(zip.namelist())):
                zip.extract(member=f, path=_directory)

        path.unlink()

        return _directory.joinpath(year)

    def _download(self, url, path):
        resp = requests.get(url, stream=True)
        if not resp.ok:
            raise resp.raise_for_status()

        total_size = int(resp.headers.get("content-length", 0))
        with path.open(mode="wb") as f:
            chunk_size = 1024
            limit = total_size / chunk_size
            for data in tqdm(resp.iter_content(chunk_size=chunk_size),
                             total=limit, unit="B", unit_scale=True):
                f.write(data)

    def extract(self, aspect_dot_element,
                year="", edinet_code="", sec_code="", jcn="",
                source_directory="", target_directory="",
                normalized=True):

        aspect, element = aspect_dot_element.split(".")

        def _extract(index, doc_id, source_dir):
            f = source_dir.joinpath(f"docs/{doc_id}.xbrl")
            try:
                text = xbrr.edinet.reader.read(f.absolute()).extract(aspect, element)
            except Exception as ex:
                print(f"Failed to parse {f.name} of {aspect_dot_element}.")

            base_name = aspect_dot_element.replace(".", "_")
            if normalized:
                file_name = f"{f.stem}_{base_name}.txt"
                content = text.value
            else:
                file_name = f"{f.stem}_{base_name}.html"
                content = text.ground

            return file_name, content
        
        return self.parse_yearly_dir(
                _extract, year, edinet_code, sec_code, jcn,
                source_directory, self._default_raw_data,
                target_directory, self._default_interim_data)

    def tokenize(self, 
                 tokenizer="janome",
                 mode="", dictionary="", dictionary_type="",
                 year="", edinet_code="", sec_code="", jcn="",
                 aspect_dot_element="",
                 source_directory="", target_directory=""):

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

        aspect_element = aspect_dot_element.replace(".", "_")
        suffix = "_" + aspect_element if aspect_element else "*"

        def _tokenize(index, doc_id, source_dir):
            file_names = []
            contents = []
            for f in source_dir.joinpath("docs").glob(f"{doc_id}{suffix}.txt"):
                tokens = []
                with f.open(encoding="utf-8") as fobj:
                    lines = fobj.readlines()
                    lines = [ln.strip() for ln in lines]
                    lines = [ln for ln in lines if ln]
                    tokens = [tokenize(ln) for ln in lines]

                file_names.append(f"{f.stem}_tokenized.txt")
                content = ""
                for ts in tokens:
                    content += "\t".join(ts) + "\n"
                contents.append(content)

            return file_names, contents

        return self.parse_yearly_dir(
                _tokenize, year, edinet_code, sec_code, jcn,
                source_directory, self._default_interim_data,
                target_directory, self._default_processed_data)


    def parse_yearly_dir(self, func,
                         year,
                         edinet_code, sec_code, jcn,
                         source_directory, default_source_path,
                         target_directory, default_target_path):

        if not source_directory:
            s_dir = Path.cwd().joinpath(default_source_path)
        else:
            s_dir = Path(source_directory)
            if not s_dir.is_absolute():
                s_dir = Path.cwd().joinpath(source_directory)

        if not target_directory:
            t_dir = Path.cwd().joinpath(default_target_path)
        else:
            t_dir = Path(target_directory)
            if not t_dir.is_absolute():
                t_dir = Path.cwd().joinpath(target_directory)
        
        years = [year] if year else []
        if len(years) == 0:
            for d in s_dir.iterdir():
                if d.is_dir():
                    years.append(d.name)

        for y in years:
            s_y_dir = s_dir.joinpath(y)
            documents = pd.read_csv(s_y_dir.joinpath("documents.csv"),
                                    sep="\t",  header=0)
            documents["sec_code"] = documents["sec_code"].astype(str)
            documents["jcn"] = documents["jcn"].astype(str)

            sec_code = str(sec_code)
            filters = {
                "edinet_code": edinet_code,
                "sec_code": sec_code + "0" if len(sec_code) == 4 else sec_code,
                "jcn": str(jcn)
            }

            for k in filters:
                if filters[k]:
                    documents = documents[documents[k] == filters[k]]

            t_y_dir = t_dir.joinpath(y)
            t_y_dir.mkdir(parents=True, exist_ok=True)
            documents.to_csv(t_y_dir.joinpath("documents.csv"),
                             header=True, index=False, sep="\t",
                             encoding="utf-8")

            t_y_dir = t_y_dir.joinpath("docs")
            t_y_dir.mkdir(exist_ok=True)
            total = len(documents)

            print(f"Fiscal year {y}")
            for i, doc_id in tqdm(iterable=documents["doc_id"].iteritems(),
                                  total=total):

                file_name, content = func(
                     index=i, doc_id=doc_id, source_dir=s_y_dir)

                file_names = []
                contents = []

                if isinstance(file_name, str) and isinstance(content, str):
                    file_names = [file_name]
                    contents = [content]
                else:
                    file_names = file_name
                    contents = content

                for f, c in zip(file_names, contents):
                    path = t_y_dir.joinpath(f)
                    with path.open("w", encoding="utf-8") as _f:
                        _f.write(c)

        return t_dir
