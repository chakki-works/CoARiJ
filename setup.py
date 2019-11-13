from setuptools import setup, find_packages


readme = ""
with open("README.md", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="coarij",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(exclude=["texts"]),
    description="Corpus of Annual Reports in Japan",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="MIT",
    url="https://github.com/chakki-works/CoARiJ",
    install_requires=[
        "edinet-python>=0.1.14",
        "fire>=0.2.1",
        "pandas>=0.25.1",
        "tqdm>=4.36.1"
    ],
    entry_points={"console_scripts": "coarij = coarij.cli:main"}
)
