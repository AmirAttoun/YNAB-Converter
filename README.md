# YNAB Converter

![YNAB Converter](https://i.ibb.co/B2pTt7p/YNAB.png)

![Language](https://img.shields.io/badge/language-python-green)\
![Language](https://img.shields.io/badge/language-fastapi-white)\
![Language](https://img.shields.io/badge/language-html-blue)\
![Language](https://img.shields.io/badge/language-jinja2-black)\
![Language](https://img.shields.io/badge/language-javascript-pink)


## Video Demo
Video Demo:  TBD

## GitHub
https://github.com/AmirAttoun/YNAB-Converter

## Introduction
Welcome to *YNAB Converter* for Migrosbank / Viseca (One) bank statements!
This project was created as the final project for edX's C50x Computer Science with Python


## Glossary
- Migrosbank: A local Swiss bank
- Vicesa (One): A credit card provider
- YNAB (https://ynab.com): A web based budgeting tool

## Description
YNAB supports the import of .csv files for adding transactions.
These transactions need to conform to the YNAB defined standards.
Migrosbank as well as Viseca (One) allow for export of transaction statements.
Those exports don't match the YNAB defined standards.

This application aims at formatting the differing individual transaction statements of said providers
to the YNAB defined ready-for-import structure.
Data such as "Memo" and "Payee" can be edited on the fly.

The application allows for quick addition of new source statements from different banks, including dynamic header mapping and further config parameterization

## Technology
This project was built using:
- FastAPI Framework
- Python
- Jinja2
- JavaScript
- Bootstrap

## Features

### Uploading a transaction statement
Users cant upload a bank statement originating from Migrosbank or Viseca (One).
Both statemtens will be processed to a uniform format.
*New .csv statement formats can easily be added!*

### Editing the transaction statement
Once a statement has been uploaded, the user is free to edit the relevant fields.
Depending on the config in main.py, certain words will be used a split point.
Relevant fields are "Memo" and "Payee". Date and the amount are not editable to ensure integrity of crucial data as noted by the transaction statement.

### Downloading the normalized transaction statement
After editing the statement, a .csv conforming to YNAB standards is generated and downloaded.
Use the YNAB import functionality for the import of this file.
Payment categories will need to be added in YNAB as the .csv import does not support this functionality.

### Future features 
- Adding additional statement providers
- User session logic

### Future optimization
- Unit tests
- Handle I/O in memory (or DB)
- Better error handling
- Reworked end points
- OOP implementation?
- Design improvements

### Requirements
See requirements.txt for mandatory pip installs.

```
pip install -r requirements. txt
```

### Usage
```
uvicorn main:app --reload
```
### CSV_CONFIG / STANDARD_HEADERS
```
# ----CONFIG----- #
# Standard headers for CSV files
STANDARD_HEADERS: List[str] = ["Datum", "Buchungstext", "Betrag", "Valuta"]

# headers: Headers to expect in the CSV file
# delimiter: Delimiter used in the CSV file
# skip_first_row: Whether to skip the first row of the CSV file
# mapping: Mapping of expected headers to standard headers
# date_conversion: Date conversion configuration
# type: Type of account (Debit or Credit)
# header_cutoff: Number of intial lines to ignore in CSV file
# initial_field: Initial field to identify the start of the CSV file in accordance with the bank chosen
# memo_cut_off: Splitpoint for the memo field


CSV_CONFIGS: Dict[str, Dict[str, Any]] = {
    "Migrosbank": {
        "headers": ["Datum", "Buchungstext", "Betrag", "Valuta"],
        "delimiter": ";",
        "skip_first_row": True,
        "mapping": {
            "Datum": "Datum",
            "Buchungstext": "Buchungstext",
            "Betrag": "Betrag",
            "Valuta": "Valuta",
        },
        "date_conversion": None,
        "type": "Debit",
        "header_cutoff": 11,
        "initial_field": "Kontoauszug bis:",
        "memo_cut_off": "Karte:",
    },
    "Viseca (One)": {
        "headers": [
            "TransactionID",
            "Date",
            "Merchant",
            "Amount",
            "PFMCategoryID",
            "PFMCategoryName",
        ],
        "delimiter": ",",
        "skip_first_row": True,
        "mapping": {
            "Date": "Valuta",
            "Merchant": "Payee",
            "Amount": "Betrag",
            "PFMCategoryName": "Buchungstext",
        },
        "date_conversion": {
            "source_format": "%Y-%m-%dT%H:%M:%S",
            "target_format": "%d.%m.%y",
        },
        "type": "Credit",
        "header_cutoff": 0,
        "initial_field": "TransactionID",
        "memo_cut_off": None,
    }
    # Other configurations as needed
}
# ----END CONFIG----- #
```

### Copyright Disclaimer
The design for the application is provided for free by https://bootstrapmade.com/free-bootstrap-coming-soon-template-countdwon/ and has been "jinjafied" and adjusted by me.
Please check https://bootstrapmade.com/license/ for further details.

### Contact
amir(dot)attoun(at)protonmail(dot)ch