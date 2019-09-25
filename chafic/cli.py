import fire
from chafic.download import download


class Chafic(object):
    """Data management tool for chaFic dataset."""

    def download(self, path="", kind="R", year=""):
        return download(path, kind, year)


if __name__ == '__main__':
    fire.Fire(Chafic)
