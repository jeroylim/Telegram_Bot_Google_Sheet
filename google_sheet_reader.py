import sys
import requests
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp

json_path = os.getenv("GOOGLE_CREDENTIALS_PATH")


# Check if file exists
if not os.path.exists(json_path):
    print("Error: The credentials file does not exist at the specified path.")
    sys.exit(1)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

sheet = client.open("Sheet_to_Tele_Bot_Test").sheet1

def return_item(asset):
    for index, assets in enumerate(sheet.col_values(1), 1):  # Iterate through column 1
        if asset.lower() == assets.lower():
            sheet.update_cell(index, 2, "")          # Clear borrower name
            sheet.update_cell(index, 4, "Available") # Update status
            sheet.update_cell(index, 5, "Storeroom") # Update location
            return f"Returned {asset.upper()} successfully"
    return "No Such Item"

def borrow_item(asset, name, location):
    for index, assets in enumerate(sheet.col_values(1), 1):
        if asset.lower() == assets.lower():
            sheet.update_cell(index, 2, name)        # Set borrower's name
            sheet.update_cell(index, 4, "In Use")    # Update status
            sheet.update_cell(index, 5, location) # Update location
            return f"Borrowed {asset.upper()} successfully"
    return "No Such Item"

#borrow_item("NB4817", "Dan Mig", "Yishun")
#return_item("NB4817")
#testing commit changes







