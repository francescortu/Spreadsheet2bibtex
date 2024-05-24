# Spreadsheet2bibtex
Simple python tool to:
    - Retrieve bibtex from the title of the paper and add the bibtex to another column
    - 
[!title tex](./images/title2bibtex.jpeg)

    - Generate .bib from a column of bibtex


## Setup
### 1. Enable Google Sheets API
- Create a project in the [Google Developers Console](https://console.cloud.google.com/projectcreate)
- [Enable the Google Sheets API](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com) in the project 
- [configure OAuth consent screen](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
- [Authorize credentials for a desktop application](https://developers.google.com/sheets/api/quickstart/python#authorize_credentials_for_a_desktop_application)