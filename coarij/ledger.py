import os
from pathlib import Path
import shutil
import time
import pandas as pd
from tqdm import tqdm
from xbrr.edinet.client.document_client import DocumentClient


class Ledger():

    def __init__(self, storage, path):
        self.storage = storage
        self.path = path
        self.data = pd.read_csv(self.path, sep="\t")
        self.data = self.data.astype({
            "fiscal_year": str,
            "sec_code": str,
            "jcn": str
        })

    def collect(self, directory="", source_directory="",
                year="", edinet_code="", sec_code="", jcn="",
                file_type="xbrl"):
        """
        Collect the documents based on ledger file.
        """

        if not source_directory:
            s_dir = Path.cwd().joinpath(self.storage._default_raw_data)
        else:
            s_dir = Path(source_directory)
            if not s_dir.is_absolute():
                s_dir = Path.cwd().joinpath(source_directory)

        target = self.data

        filters = {
            "fiscal_year": str(year),
            "edinet_code": edinet_code,
            "sec_code": str(sec_code),
            "jcn": str(jcn)
        }

        conditions = []
        for k in filters:
            if filters[k]:
                target = target[target[k] == filters[k]]
                conditions.append(filters[k])

        if len(conditions) == 0:
            raise Exception("You have to specify at least one condition.")

        if not directory:
            t_dir = Path.cwd().joinpath(self.storage._default_raw_data)
        else:
            t_dir = Path(directory)
            if not t_dir.is_absolute():
                t_dir = Path.cwd().joinpath(directory)

        t_dir = t_dir.joinpath("_".join(conditions))
        if not t_dir.exists():
            t_dir.mkdir(parents=True, exist_ok=True)

        for i, r in tqdm(target.iterrows(), total=target.shape[0]):
            fiscal_year = r["fiscal_year"]
            doc_id = r["doc_id"]
            y_s_dir = s_dir.joinpath(fiscal_year).joinpath("docs")
            y_s_path = y_s_dir.joinpath(f"{doc_id}.xbrl")

            if y_s_path.exists():
                shutil.copy(str(y_s_path), str(t_dir.joinpath(f"{doc_id}.xbrl")))
            else:
                client = DocumentClient()
                if file_type == "pdf":
                    file_path = client.get_pdf(doc_id, save_dir=t_dir)
                elif file_type == "xbrl":
                    file_path = client.get_xbrl(doc_id, save_dir=t_dir,
                            expand_level="file")
                elif file_type == "zip":
                    file_path = client.get_xbrl(doc_id, save_dir=t_dir,
                            expand_level="dir")
                elif file_type == "csr":
                    if isinstance(r['csr_path'], str) and r['csr_path']:
                        print(r['csr_path'])
                        file_name = os.path.basename(r['csr_path'])
                        url = f"https://s3-ap-northeast-1.amazonaws.com/chakki.esg.csr.jp/{r['csr_path']}"
                        self.storage._download(url, t_dir.joinpath(file_name))
                else:
                    raise Exception(f"File type {file_type} is not supported")
                time.sleep(0.1)  # to save api host

        return target
