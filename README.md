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

The application allows for quick addition of new source statements from different banks, including dynamic header mapping and further config parameterization.

## Technology
This project was built using:
- FastAPI Framework
- Python
- Jinja2
- JavaScript

## Features

### Uploading a transaction statement
Users cant upload a bank statement originating from Migrosbank or Viseca (One).
Both statemtens will be processed to a uniform format.
*New .csv statement formats can easily be added!*

### Editing the transaction statement
Once a statement has been uploaded, the user is free to edit the relevant fields.
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
- Better Error Handling
- User session logic

### Requirements
See requirements.txt for mandatory pip installs

### Usage
```
uvicorn main:app --reload
```

### Contact
amir(dot)attoun(at)protonmail(dot)ch