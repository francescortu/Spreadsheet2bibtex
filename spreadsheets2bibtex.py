import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

GREEN = "\033[92m"
ENDC = "\033[0m"

import os
from dotenv import load_dotenv

load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
INPUT_RANGE = os.getenv("INPUT_RANGE")
OUTPUT_RANGE = os.getenv("OUTPUT_RANGE")

parser = argparse.ArgumentParser()
parser.add_argument("--bib", action="store_true", help="bolean switch") 

def process_values(values):
    # for each value extract the id of the paper
    arxiv_ids = []
    for row in values:
        try:
            arxiv_ids.append(row[0].split("]")[0][1:])
        except:
            arxiv_ids.append("null")

        # check if the id is a valid arxiv id (4 digits, a dot, 4 digits)
        if len(arxiv_ids[-1]) != 10:
            arxiv_ids[-1] = "null"

    print(
        f"{GREEN} Retrieved {len(arxiv_ids) - len([id for id in arxiv_ids if id=='null'])} id and found {len([id for id in arxiv_ids if id=='null'])} null values {ENDC}"
    )
    # use d2b command line to get the bibtex
    bibtex = []
    for id in arxiv_ids:
        if id != "null":
            bibtex.append(os.popen(f"d2b {id} --plain").read())
        else:
            bibtex.append("null")
            
        if "Could not get data from dblp." in bibtex[-1]:
            bibtex[-1] = "null"
    # write the bibtex to the spreadsheet
    creds = None
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        body = {"values": [[x] for x in bibtex]}
        result = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=OUTPUT_RANGE,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
    except HttpError as err:
        print(err)


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        if args.bib:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SPREADSHEET_ID, range=OUTPUT_RANGE)
                .execute()
            )
            values = result.get("values", [])
            
            #save in output.bib
            with open("output.bib", "+w") as f:
                for v in values:
                    if len(v) >= 1:
                        f.write(v[0])
                    else:
                        continue
            
        else:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SPREADSHEET_ID, range=INPUT_RANGE)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            
            process_values(values)
        
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    args = parser.parse_args()
    main()
