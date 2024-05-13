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
Welcome to the *YNAB Converter* for Migrosbank / Viseca One bank statements!
This project was created as the final project for edX's CS50x: Introduction to Computer Science.

## Glossary
- Migrosbank (https://www.migrosbank.ch): A local Swiss bank
- Viseca One (https://www.viseca.ch/de): A credit card provider
- YNAB (https://ynab.com): A web-based budgeting tool

## Description
YNAB supports the import of .csv files for adding transactions.
These transactions need to conform to YNAB defined standards.
Migrosbank and Viseca One allow for the export of transaction statements.
These exports do not match the YNAB defined standards.

This application aims at formatting the differing individual transaction statements of said providers
to the YNAB defined ready-for-import structure.
Data fields such as "Memo" and "Payee" are editable in real-time.

The application allows for the quick addition of new source statements from different banks, including dynamic header mapping and further configuration parameterization.

## Technology
This project was built using:
- FastAPI Framework
- Python
- Jinja2
- JavaScript
- Bootstrap

## Features

### Uploading a transaction statement
Users can upload a bank statement originating from Migrosbank or Viseca One.
Both statements will be processed to a uniform format.
New .csv statement formats can easily be added!

### Editing the transaction statement
Once a statement has been uploaded, the user is free to edit the relevant fields.
Depending on the configuration in main.py, certain words will be used as split points.
Relevant fields are "Memo" and "Payee". Date and the amount are not editable to ensure the integrity of crucial data as noted by the transaction statement.

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
    - Improved file validation is needed
- Reworked endpoints
- OOP implementation?
- Design improvements
- Suggestions for Payees after upload

### Thoughts on the implementation
As a first FastAPI project, I am pleased with the results.
My tendency to jump into the code and figure out critical structural decisions later manifested itself again.
Therefore, the code is a lot messier and unoptimized as well.

For example, the decision to configure variables in the consts CSV_CONFIG and STANDARD_HEADERS is a good one but is fairly basic.
Much nicer would be the option to upload a csv, and let the user map the required output headers to the input file dynamically through the GUI. This way no strict pre-config would be necessary.
I'm also not completely happy with the implementation of the endpoints. I'm especially annoyed that after the file upload, I had to resort to JavaScript to handle the redirect to /thankyou. I would much prefer to handle this logic all in FastAPI.
In many ways, I still need to discover a lot about FastAPI.

Additionally, I still do not like CSS one bit. Bootstrap is nice though.

### Requirements
See requirements.txt for mandatory pip installs.
```
pip install -r requirements.txt
```

### Usage
```
uvicorn main:app --reload
```

### File and folder listings
- main.py 
    - contains the main logic in the form of routes. This file also contains the import CSV_CONFIG and STANDARD_HEADERS constants for defining .csv import templates.
- helpers.py 
    - contains the core logic for reading and normalizing the input. The file also includes a custom exception in the form of Class Message(). I use this class to dynamically call the error.html template with a custom message. In retrospect, FastAPI could do this through HTTP Exceptions. Additionally, this file contains a function to delete the temporarily stored bank statements after the upload.
- templates/ 
    - contains all html templates. The base layout is provided through layout.html. The other templates extend the base layout.
- static/ 
    - contains all css, img, js, and vendor files. This includes a local version of bootstrap. The main.js is the only JS code used and provides two functions. One of them is a redirect which I could not achieve through FastAPI since it is not feasible to return a template after the HTTP response is done. The other function displays a countdown on the thankyou.html as well as a redirect to root.
- sample_uploads/ 
    - contains two sample transaction statements for testing purposes.
- files/ 
    - temporarily stores the uploaded and converted transaction statement. This directory is flushed immediately after the upload of the initial file.


### CSV_CONFIG / STANDARD_HEADERS
```
# ----CONFIG----- #
# Standard headers for CSV files
STANDARD_HEADERS: List[str] = ["Datum", "Buchungstext", "Betrag", "Valuta"]

# Headers: Expected headers in the CSV file
# Delimiter: Character used to separate fields in the CSV
# Skip_first_row: Whether to skip the first row (typically headers)
# Mapping: Links CSV headers to standard headers
# Date_conversion: Configuration for date formatting
# Type: Account type (Debit or Credit)
# Header_cutoff: Number of initial lines to skip (excluding header)
# Initial_field: Identifier for the start of data in the CSV (for validation purposes)
# Memo_cut_off: Delimiter for splitting the memo field


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

### Copyright Disclaimer Design Template
The design for the application is provided for free by https://bootstrapmade.com/free-bootstrap-coming-soon-template-countdwon/ and has been "jinjafied" and adjusted by me.
Please check https://bootstrapmade.com/license/ for further details.

### Contact
amir(dot)attoun(at)protonmail(dot)ch