from fastapi import Request, UploadFile, BackgroundTasks
from pathlib import Path
from fastapi.responses import HTMLResponse, FileResponse
import csv, os

from helpers import app, templates, Message, read_and_normalize_csv_data, delete_file

# TODO Validate if valid CSV (Migrosbank or Viseca) []
# TODO Delete File on server [X]
# Use background task to delete file
# Verify Usage of BackgroundTasks


# Constants
# Path() --> Root Directory
UPLOAD_DIR = Path() / "uploads"
CONVERT_DIR = Path() / "converted"
BANKS = ["Migrosbank", "Viseca (One)"]
FILETYPES = [".CSV", ".csv"]


STANDARD_HEADERS = ["Datum", "Buchungstext", "Betrag", "Valuta"]

CSV_CONFIGS = {
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
        "header_cutoff": 12,
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
    }
    # Other configurations as needed
}


# Root Explorer, pass BANKS for valid banks
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"banks": BANKS}
    )


# Upload CSV, validate for valid input (not empty and must be a csv)
@app.post("/uploadfile")
async def create_upload_file(file_upload: UploadFile, request: Request):
    # Get the selected bank
    form_data = await request.form()
    bank = form_data.get("banks")

    data = await file_upload.read()
    # Check if a file was provided
    if not data:
        raise Message("You did not provide any file!")
    elif not file_upload.filename.lower().endswith(tuple(FILETYPES)):
        raise Message("You did not provide a .csv file!")
    else:
        # TODO CHECK IF VALID CSV

        save_to = UPLOAD_DIR / file_upload.filename
        with open(save_to, "wb") as f:
            f.write(data)

        # Open the file and pass it to verify

        # Read the csv
        filedata = read_and_normalize_csv_data(
            UPLOAD_DIR / file_upload.filename, bank, CSV_CONFIGS, STANDARD_HEADERS
        )

        config = CSV_CONFIGS.get(bank)
        account_type = config.get("type")

        return templates.TemplateResponse(
            request=request,
            name="verify.html",
            context={"filedata": filedata, "account_type": account_type},
        )


@app.post("/download-file")
async def download_file(request: Request, background_tasks: BackgroundTasks):
    form_data = await request.form()
    filedata = []

    # Extract the data from the form
    i = 1
    while f"buchungstext_{i}" in form_data:
        outflow = form_data.get(f"outflow_{i}")
        if outflow and outflow.startswith("-"):
            outflow = outflow.lstrip("-")
        entry = {
            "Date": form_data.get(f"valuta_{i}"),
            "Payee": form_data.get(f"payee_{i}"),
            "Memo": form_data.get(f"buchungstext_{i}"),
            "Outflow": outflow,
            "Inflow": form_data.get(f"inflow_{i}"),
        }
        filedata.append(entry)
        i += 1

    # Write the data to a new CSV file
    filename = CONVERT_DIR / "updated_data.csv"

    with open(filename, "w", newline="", encoding="iso-8859-1") as f:
        if filedata:
            writer = csv.DictWriter(f, fieldnames=filedata[0].keys())
            writer.writeheader()
            writer.writerows(filedata)
        else:
            raise Message("No data to write to CSV file")

    # When FileResponse is returned, it will trigger a download, and the file will be deleted afterwards
    # Return a FileResponse to start the download
    response = FileResponse(
        filename, media_type="text/csv", filename=os.path.basename(filename)
    )

    # Delete file on server, using background task
    background_tasks.add_task(delete_file, filename)

    return response
