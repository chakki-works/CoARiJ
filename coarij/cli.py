import fire
from coarij.storage import Storage


class CoARiJ(object):
    """
    Data management tool for CoARiJ
     dataset.
    """

    def __init__(self):
        self._storage = Storage()

    def download(self, directory="", kind="F", year="", force=False):
        """Download the {kind} {year} dataset to {directory}.

        Args:
            directory (str): Downloaded dataset to specified directory.
            kind (str): 'F': raw file datadata, 'E': text extracted data.
            year (str): Financial year of dataset.
            force (bool): When True, overwrite data if exist.

        Returns:
            str: Path to downloaded directory

        """
        return self._storage.download(directory, kind, year, force)

    def extract(self, aspect_element,
                year="", edinet_code="", sec_code="", jcn="",
                source_directory="", target_directory="",                
                normalized=True):
        """
        Extract {aspect_to_element} from files in {source_directory}{year} and
        save it in {target_directory}{year} as txt/html file.

        Args:
            aspect_element (str): Target aspect.element (ex: company.history).
            year (str): Target financial year.
            edinet_code (str): EDINET code to specify compan.
            sec_code (str): SEC code to specify compan.
            jcn (str): Target JCN code to specify compan.
            source_directory (str): Source directory includes XBRL files.
            target_directory (str): Target directory that txt/htmls are saved.
            normalized: (bool): True: extract text, False: save raw xml(html).

        Returns:
            str: Path to extracted files directory

        """

        return self._storage.extract(
            aspect_dot_element=aspect_element, 
            year=year, edinet_code=edinet_code, sec_code=sec_code, jcn=jcn,
            source_directory=source_directory, target_directory=target_directory,
            normalized=normalized)

    def tokenize(self, tokenizer="janome",
                 mode="", dictionary="", dictionary_type="",
                 year="", edinet_code="", sec_code="", jcn="",
                 aspect_element="",
                 source_directory="", target_directory=""):
        """
        Tokenize by {tokenizer} from files in {source_directory}{year} and
        save it in {target_directory}{year} as txt/html file.

        Args:
            tokenizer (str): Japanese tokenizer ('janome' or 'sudachi').
            mode: (str): Sudachi tokenizer mode.
            dictionary: (str): Dictionary path for Janome.
            dictionary_type: (str): Dictionary type for Janome.
            year (str): Target financial year.
            edinet_code (str): EDINET code to specify compan.
            sec_code (str): SEC code to specify compan.
            jcn (str): Target JCN code to specify compan.
            aspect_element (str): Target aspect.element (ex: company.history).
            source_directory (str): Source directory includes XBRL files.
            target_directory (str): Target directory that txt/htmls are saved.

        Returns:
            str: Path to tokenized files directory

        """
        return self._storage.tokenize(
            tokenizer=tokenizer,
            mode=mode, dictionary=dictionary, dictionary_type=dictionary_type,
            year=year, edinet_code=edinet_code, sec_code=sec_code, jcn=jcn,
            aspect_dot_element=aspect_element,
            source_directory=source_directory, target_directory=target_directory)


def main():
    fire.Fire(CoARiJ)


if __name__ == "__main__":
    main()
