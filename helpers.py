from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv, os
from datetime import datetime

# ----- TODO Summary -------
# [X] Adjust Migrosbank header cut off
# TODO Document Parameters and Return Values []
# TODO Docstrings for Functions []
# TODO Add Type Hints []
# TODO Test long statement files []
# TODO Adjut output name to include bank name [X]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Message(Exception):
    def __init__(self, message: str):
        self.message = message


# Exception handler for CustomError
@app.exception_handler(Message)
def custom_error_handler(request: Request, exc: Message):
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,  # Even though not used, it needs to be passed to TemplateResponse
            "message": exc.message,
        },
        status_code=400,
    )


def convert_date(timestamp):
    # Convert the ISO 8601 format to dd-mm-yy
    dt_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    return dt_object.strftime("%d-%m-%y")


def delete_file(name: str):
    """Background task function for deleting a file."""
    os.remove(name)


def normalize_data(data, mapping, standard_headers, config):
    normalized_data = []
    date_conversion_config = config.get(
        "date_conversion"
    )  # Get date conversion info from the config

    for entry in data:
        normalized_entry = {}
        for source, standard in mapping.items():
            if source in entry:
                # Check if this field is a date needing conversion and if a conversion config exists
                if source == "Date" and date_conversion_config:
                    try:
                        # Apply date conversion using the specified source and target formats
                        dt_object = datetime.strptime(
                            entry[source], date_conversion_config["source_format"]
                        )
                        normalized_entry[standard] = dt_object.strftime(
                            date_conversion_config["target_format"]
                        )
                    except ValueError:
                        # Handle cases where date conversion fails
                        normalized_entry[standard] = None
                else:
                    # No conversion needed, transfer data as is
                    normalized_entry[standard] = entry[source]
                    # This never gets triggered?
            else:
                # Ensure field exists in normalized_entry, even if source is not in entry
                normalized_entry[standard] = None

        # Ensure all standard headers are present in the normalized_entry, otherwise set to empty string
        for header in standard_headers:
            if header not in normalized_entry:
                normalized_entry[header] = ""

        normalized_data.append(normalized_entry)

    return normalized_data


def read_and_normalize_csv_data(file_path, bank, csv_configs, STANDARD_HEADERS):
    config = csv_configs.get(bank)
    if not config:
        raise Message(f"You have not selected a valid bank!")

    # TODO if Migrosbank cut off a certain amount of lines

    with open(file_path, newline="", encoding="iso-8859-1") as csvfile:
        if config["headers"]:
            reader = csv.DictReader(
                csvfile, fieldnames=config["headers"], delimiter=config["delimiter"]
            )
            # First, we skip the amount of rows defined in config['header_cutoff']
            # TODO Validate that there is a valid CSV (length of header)
            for i in range(config["header_cutoff"]):
                next(reader)

            # Here we are skipping the first rows if it's a header
            if config["skip_first_row"]:
                next(reader)  # Skip if it's just data
        else:
            reader = csv.DictReader(
                csvfile, delimiter=config["delimiter"]
            )  # Headers in file

        data = [row for row in reader]

    normalized_data = normalize_data(data, config["mapping"], STANDARD_HEADERS, config)
    return normalized_data
