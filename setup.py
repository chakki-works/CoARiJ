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
        "xbrr>=0.2.7",
        "fire>=0.2.1"
    ],
    entry_points={"console_scripts": "coarij = coarij.cli:main"}
)
