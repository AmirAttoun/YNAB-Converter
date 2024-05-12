# YNAB Converter

![Language](https://img.shields.io/badge/language-python-blue)\
![Language](https://img.shields.io/badge/language-fastapi-white)\
![Language](https://img.shields.io/badge/language-html-blue)\
![Language](https://img.shields.io/badge/language-jinja2-black)\
![Language](https://img.shields.io/badge/language-javascript-pink)\


## Video Demo
Video Demo:  TBD

## GitHub
https://github.com/AmirAttoun/YNAB-Converter

## Introduction
Welcome to *YNAB Converter* for Migrosbank / Viseca (One) bank statements!
This project was created as the final project for Edx's C50x Computer Science with Python

## Technology
This project was built using:
    - FastAPI Framework
    - Python
    - Jinja2
    - JavaScript

## Glossary
Migrosbank – A local Swiss bank
Vicesa (One) – A credit card provider
YNAB (https://ynab.com) – A web based budgeting tool

## Description

YNAB supports the import of csv files for importing transactions.
These transactions need to conform to the YNAB defined standards.
Migrosbank as well as Viseca (One) allow for export of transaction statements.
This application aims at formatting the differing individual transaction statements of said providers
to the YNAB defined ready-for-import structure.

The application allows for quick addition of new source statements from different banks, including dynamic header mapping and further config parameterization.

## Features

### Uploading a transaction statement
Users cant upload bank statement originating from Migrosbank or Viseca (One).
Both statemtens will be processed to a uniform format.

### Editing the transaction statement
Once a statement has been uploaded, the user is free to edit the relevant fields.
Relevant fields are "Memo" and "Payee".

### Download the transaction statement
After editing the statement, a YNAB standardized .csv can be downloaded.

### Future features 

- Adding additional statement providers
- User session logic

### Future Optimization
- Unit tests
- Handle I/O in memory (or DB))
- Better Error Handling
- User session logic

### Contact
Please do not hesitate to contact me if you have questions regarding the project
or any other related subject. Mail me <a href="mailto:amir.attoun@protonmail.ch">here</a>.