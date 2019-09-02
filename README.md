# chaFiC: chakki Financial Report Corpus

We organized Japanese financial reports to encourage applying NLP techniques to the financial domain.

## Dataset

The corpora are separated to each financial years.

* [2014]()
* [2015]()
* [2016]()
* [2017]()
* [2018]()

## Statistics

| fiscal_year | num_financial | num_csr | 
|-------------|---------------|---------| 
| 2014        | 3885          | 86      | 
| 2015        | 3579          | 84      | 
| 2016        | 4041          | 99      | 
| 2017        | 1515          | 28      | 
| 2018        | 3005          | 48      | 

### Content

Each dataset includes following files.

* XBRL file of annual reports (files are retrieved from [EDINET]).
* PDF file of CSR reports (additional content).

The structure of each dataset is following.

```
chakki_esg_financial_{year}.zip
└──{year}
     ├── documents.csv
     └── docs/
```

`documents.csv` has following columns.

Examples:

* edinet_code: `E0000X`
* filer_name: `XXX株式会社`
* fiscal_year: `201X`
* fiscal_period: `FY`
* doc_path: `docs/S000000X.xbrl`
* csr_path: `docs/E0000X_201X_JP_36.pdf`

## Data Extraction

We offer the raw XBRL/PDF file to preserve all of the contents.

We offer the raw XBRL/PDF file to preserve all of the contents. But we understand these are terrible to use.

For that reason, we offer the pipeline to extract contents from the raw file. We develop parser in the separated repository [edinet-python](https://github.com/chakki-works/edinet-python). You can use [edinet-python](https://github.com/chakki-works/edinet-python) as independent parser for XBRL.

### Supported Elements

Please refer the [edinet-python](https://github.com/chakki-works/edinet-python) README.md.

Example:

Extract ``s from XBRLs.

```py
python xxx.py y_Element
```

## Utilize Data for NLP

We offer the parser for the financial documents based on [GiNZA](https://github.com/megagonlabs/ginza). Please refer the [ficser](https://github.com/chakki-works/ficser) to use this feature.

Example: Parse

```py
```

Example: NER

```py
```
