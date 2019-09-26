# chaFiC: chakki Financial Report Corpus

We organized Japanese financial reports to encourage applying NLP techniques to financial analytics.

## Dataset

You can download dataset by command line tool.

```
pip install chafic
```

```

```

### Raw dataset file

The corpora are separated to each financial years.

| fiscal_year | Raw file version | Text extracted version | 
|-------------|-------------------|-----------------|
| 2014        | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2014.zip)          | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2014.zip)              | 
| 2015        | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2015.zip)          | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2015.zip)        | 
| 2016        | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2016.zip)          | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2016.zip)              | 
| 2017        | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2017.zip)          | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2017.zip)        | 
| 2018        | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_2018.zip)          | [.zip](https://s3-ap-northeast-1.amazonaws.com/chakki.esg.financial.jp/dataset/release/chakki_esg_financial_extracted_2018.zip)        | 


## Statistics

| fiscal_year | number_of_reports | has_csr_reports | has_financial_data | has_stock_data | 
|-------------|-------------------|-----------------|--------------------|----------------| 
| 2014        | 3724              | 92              | 3583               | 3595           | 
| 2015        | 3870              | 96              | 3725               | 3751           | 
| 2016        | 4066              | 97              | 3924               | 3941           | 
| 2017        | 3578              | 89              | 3441               | 3472           | 
| 2018        | 3513              | 70              | 2893               | 3413           | 


### Content

**Raw file version**

The structure of dataset is following.

```
chakki_esg_financial_{year}.zip
└──{year}
     ├── documents.csv
     └── docs/
```

`docs` includes XBRL and PDF file.

* XBRL file of annual reports (files are retrieved from [EDINET]).
* PDF file of CSR reports (additional content).

`documents.csv` has metadata like following.

* edinet_code: `E0000X`
* filer_name: `XXX株式会社`
* fiscal_year: `201X`
* fiscal_period: `FY`
* doc_path: `docs/S000000X.xbrl`
* csr_path: `docs/E0000X_201X_JP_36.pdf`

**Text extracted version**

Text extracted version includes `txt` files that match each part of an annual report.  
The extracted parts are defined at [`edinet-python`](https://github.com/chakki-works/edinet-python#2-extract-contents-from-xbrl).

```
chakki_esg_financial_{year}_extracted.zip
└──{year}
     ├── documents.csv
     └── docs/
```

## Utilize Data for NLP

We offer the parser for the financial documents based on [GiNZA](https://github.com/megagonlabs/ginza). Please refer the [ficser](https://github.com/chakki-works/ficser) to use this feature.

Example: Parse

```py
```

Example: NER

```py
```
