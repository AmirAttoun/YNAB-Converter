from fastapi import Request, UploadFile, BackgroundTasks, Cookie, Response
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from typing import List, Dict, Any
import csv, os

from helpers import (
    app,
    templates,
    Message,
    read_and_normalize_csv_data,
    delete_all_files_in_folder,
)

# ----CONFIG----- #

UPLOAD_DIR = Path() / "files"  # Directory to store uploaded and converted files
BANKS: List[str] = ["Migrosbank", "Viseca (One)"]  # List of supported banks
FILETYPES: List[str] = [".CSV", ".csv"]  # List of supported file types

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
# ----ROUTES----- #


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """
    Serve the index page with a list of valid banks.

    Args:
        request (Request): The request context.

    Returns:
        HTMLResponse: The HTML response containing the rendered index page.
    """

    return templates.TemplateResponse(
        request=request, name="index.html", context={"banks": BANKS}
    )

@app.post("/uploadfile")
async def create_upload_file(file_upload: UploadFile, request: Request, background_tasks: BackgroundTasks) -> HTMLResponse:
    """
    Handle the upload of a CSV file, validate it, and prepare data for display.

    Args:
        file_upload (UploadFile): The uploaded CSV file.
        request (Request): The request context to retrieve additional form data.

    Raises:
        Message: Custom exception for errors related to file upload and validation.

    Returns:
        HTMLResponse: The HTML response displaying the verification page with parsed data.
    """

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
        # Get the bank configuration

        save_to = UPLOAD_DIR / file_upload.filename
        with open(save_to, "wb") as f:
            f.write(data)

        # Read the csv
        filedata = read_and_normalize_csv_data(
            UPLOAD_DIR / file_upload.filename, bank, CSV_CONFIGS, STANDARD_HEADERS
        )

        config = CSV_CONFIGS.get(bank)
        account_type = config.get("type")

        #Delete all files in the upload directory once on verify
        background_tasks.add_task(delete_all_files_in_folder, UPLOAD_DIR)

        return templates.TemplateResponse(
            request=request,
            name="verify.html",
            context={"filedata": filedata, "account_type": account_type, "bank": bank},
        )


@app.post("/download-file")
async def download_file(
    request: Request, background_tasks: BackgroundTasks) -> FileResponse:
    """
    Generate a CSV file from user-edited data and initiate a download.
    Delete all files in the upload directory after the download.

    Args:
        request (Request): The request context to retrieve form data.
        background_tasks (BackgroundTasks): Background tasks for post-response actions, like file cleanup.

    Raises:
        Message: Custom exception if there is no data to write to the CSV file.

    Returns:
        FileResponse: A response object that allows the user to download the generated CSV file.
    """

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
    bank = form_data.get("bank")
    filename = UPLOAD_DIR / f"{bank}_YNAB_data.csv"

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

     #Delete all files in the upload directory once downloaded
    background_tasks.add_task(delete_all_files_in_folder, UPLOAD_DIR)
    response.set_cookie(key="downloaded", value="true", max_age=300)  # Valid for 5 minutes
    return response

@app.get("/check-download")
async def check_download(response: Response, downloaded: bool = Cookie(default=False)):
    if downloaded:
        response.delete_cookie(key="downloaded")  # Clear the cookie after checking
        return templates.TemplateResponse("thankyou.html", {})
    else:
        return {"message": "No download initiated"}

@app.get("/thankyou")
async def thankyou(request: Request):
    return templates.TemplateResponse(
        request=request, name="thankyou.html", context={}
    )
# ----END ROUTES----- #
