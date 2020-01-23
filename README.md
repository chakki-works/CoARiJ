# CoARiJ: Corpus of Annual Reports in Japan

[![PyPI version](https://badge.fury.io/py/coarij.svg)](https://badge.fury.io/py/coarij)
[![Build Status](https://travis-ci.org/chakki-works/coarij.svg?branch=master)](https://travis-ci.org/chakki-works/coarij)
[![codecov](https://codecov.io/gh/chakki-works/coarij/branch/master/graph/badge.svg)](https://codecov.io/gh/chakki-works/coarij)

We organized Japanese financial reports to encourage applying NLP techniques to financial analytics.

## Dataset

You can download dataset by command line tool.

```
pip install coarij
```

Please refer the usage by `--` (using [fire](https://github.com/google/python-fire)).

```
coarij --
```

Example command.

```bash
# Download raw file version dataset of 2014.
coarij download --kind F --year 2014

# Extract business.overview_of_result part of TIS.Inc (sec code=3626).
coarij extract business.overview_of_result --sec_code 3626

# Tokenize text by Janome (`janome` or `sudachi` is supported).
pip install janome
coarij tokenize --tokenizer janome

# Show tokenized result (words are separated by \t).
head -n 5 data/processed/2014/docs/S100552V_business_overview_of_result_tokenized.txt
1       【      業績    等      の      概要    】
(       1       )               業績
当      連結    会計    年度    における        我が国  経済    は      、     消費    税率    引上げ  に      伴う    駆け込み        需要    の      反動   や      海外    景気    動向    に対する        先行き  懸念    等      から   弱い    動き    も      見      られ    まし    た      が      、      企業   収益    の      改善    等      により  全体  ...
```

* About the parsable part, please refer the [`xbrr`](https://github.com/chakki-works/xbrr/blob/master/docs/edinet.md).

You can use `Ledger` to select your necessary file from overall CoARiJ dataset.

```python
from coarij.storage import Storage


storage = Storage("your/data/directory")
ledger = storage.get_ledger()
collected = ledger.collect(edinet_code="E00021")
```


### Raw dataset file

The corpora are separated to each financial years.

| fiscal_year | Raw file version (F) | Text extracted version (E) | 
|-------------|-------------------|-----------------|
| 2014        | [.zip (9.3GB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2014.zip)          | [.zip (269.9MB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2014.zip)              | 
| 2015        | [.zip (9.8GB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2015.zip)          | [.zip (291.1MB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2015.zip)        | 
| 2016        | [.zip (10.2GB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2016.zip)          | [.zip (334.7MB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2016.zip)              | 
| 2017        | [.zip (9.1GB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2017.zip)          | [.zip (309.4MB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2017.zip)        | 
| 2018        | [.zip (10.5GB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2018.zip)          | [.zip (260.9MB)](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2018.zip)        | 


## Statistics

| fiscal_year | number_of_reports | has_csr_reports | has_financial_data | has_stock_data | 
|-------------|-------------------|-----------------|--------------------|----------------| 
| 2014        | 3,724             | 92              | 3,583              | 3,595           | 
| 2015        | 3,870             | 96              | 3,725              | 3,751           | 
| 2016        | 4,066             | 97              | 3,924              | 3,941           | 
| 2017        | 3,578             | 89              | 3,441              | 3,472           | 
| 2018        | 3,513             | 70              | 2,893              | 3,413           | 

* financial data is from [決算短信情報](http://db-ec.jpx.co.jp/category/C027/).
  * We use non-cosolidated data if it exist.
* stock data is from [月間相場表（内国株式）](http://db-ec.jpx.co.jp/category/C021/STAT1002.html).
  * `close` is fiscal period end and `open` is 1 year before of it.

## Content

### Raw file version (`--kind F`)

The structure of dataset is following.

```
chakki_esg_financial_{year}.zip
└──{year}
     ├── documents.csv
     └── docs/
```

`docs` includes XBRL and PDF file.

* XBRL file of annual reports (files are retrieved from [EDINET](http://disclosure.edinet-fsa.go.jp/)).
* PDF file of CSR reports (additional content).

`documents.csv` has metadata like following.

* edinet_code: `E0000X`
* filer_name: `XXX株式会社`
* fiscal_year: `201X`
* fiscal_period: `FY`
* doc_path: `docs/S000000X.xbrl`
* csr_path: `docs/E0000X_201X_JP_36.pdf`

### Text extracted version (`--kind E`)

Text extracted version includes `txt` files that match each part of an annual report.  
The extracted parts are defined at [`xbrr`](https://github.com/chakki-works/xbrr/blob/master/docs/edinet.md).

```
chakki_esg_financial_{year}_extracted.zip
└──{year}
     ├── documents.csv
     └── docs/
```
