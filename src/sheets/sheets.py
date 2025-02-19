import gspread_asyncio
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import asyncio
from datetime import datetime
from aioify import aioify
from dotenv import load_dotenv

SHEET_NAME = "Pi-Bot Administrative Sheet"

def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json",
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

aios = aioify(obj=os, name='aios')

async def get_worksheet():
    """Returns the Pi-Bot Administrative Sheet, accessible to Pi-Bot administrators."""
    agc = await agcm.authorize()
    return await agc.open(SHEET_NAME)

async def build_service_account():
    """Builds the service account used to access the administrative sheet."""
    load_dotenv()
    dev_mode = await aios.getenv('DEV_MODE') == "TRUE"
    if dev_mode:
        data = {
            "type": "service_account",
            "project_id": os.getenv('GCP_PROJECT_ID'),
            "private_key_id": os.getenv('GCP_PRIVATE_KEY_ID'),
            "private_key": os.getenv('GCP_PRIVATE_KEY'),
            "client_email": os.getenv('GCP_CLIENT_EMAIL'),
            "client_id": os.getenv('GCP_CLIENT_ID'),
            "auth_uri": os.getenv('GCP_AUTH_URI'),
            "token_uri": os.getenv('GCP_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('GCP_AUTH_PROVIDER_X509'),
            "client_x509_cert_url": os.getenv('GCP_CLIENT_X509_CERT_URL')
        }
    else:
        data = {
            "type": "service_account",
            "project_id": os.getenv('GCP_PROJECT_ID'),
            "private_key_id": os.getenv('GCP_PRIVATE_KEY_ID'),
            "private_key": f"{os.getenv('GCP_PRIVATE_KEY')}".encode().decode('unicode_escape'),
            "client_email": os.getenv('GCP_CLIENT_EMAIL'),
            "client_id": os.getenv('GCP_CLIENT_ID'),
            "auth_uri": os.getenv('GCP_AUTH_URI'),
            "token_uri": os.getenv('GCP_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('GCP_AUTH_PROVIDER_X509'),
            "client_x509_cert_url": os.getenv('GCP_CLIENT_X509_CERT_URL')
        }
    with open("service_account.json",'w+') as f:
        json.dump(data, f)
    print("Service account built.")

async def send_variables(data_arr, type):
    """Sends variable backups to the Administrative Sheet."""
    agc = await agcm.authorize()
    ss = await agc.open(SHEET_NAME)
    if type == "variable":
        var_sheet = await ss.worksheet("Variable Backup")
        await var_sheet.batch_update([{
            'range': "C3:C8",
            'values': data_arr
        }])
        print("Stored variables in Google Sheet.")
    elif type == "store":
        stored_var_sheet = await ss.worksheet("Stored Variable Backup")
        await stored_var_sheet.append_row([str(datetime.now())] + [v[0] for v in data_arr])
        print("Stored variables in the long-term area.")

async def get_variables():
    """Gets the previous variables, so that when Pi-Bot is restarted, the ping information is not lost."""
    agc = await agcm.authorize()
    ss = await agc.open(SHEET_NAME)
    var_sheet = await ss.worksheet("Variable Backup")
    data_arr = await var_sheet.batch_get(["C3:C8"])
    data_arr = data_arr[0]
    for row in data_arr:
        row[0] = json.loads(row[0])
    return data_arr

async def getStarted():
    await build_service_account()
    agc = await agcm.authorize()
    ss = await agc.open("Pi-Bot Administrative Sheet")
    print("Initialized gspread.")

async def get_raw_censor():
    ss = await get_worksheet()
    event_sheet = await ss.worksheet("Censor Management")
    words = await event_sheet.batch_get(["B3:C1000"])
    return words

async def get_tags():
    ss = await get_worksheet()
    tag_sheet = await ss.worksheet("Tags")
    tags = await tag_sheet.batch_get(["B3:E1000"])
    tags = tags[0]
    res = []
    for row in tags:
        res.append({
            'name': row[0],
            'text': row[1],
            'launch_helpers': row[2] == "Y",
            'members': row[3] == "Y"
        })
    return res

async def updateWikiPage(title):
    ss = await get_worksheet()
    var_sheet = await ss.worksheet("Variable Backup")
    await var_sheet.update_acell('C30', title)

async def getWikiPage():
    ss = await get_worksheet()
    var_sheet = await ss.worksheet("Variable Backup")
    res = await var_sheet.batch_get(["C30"])
    return res[0][0][0]

event_loop = asyncio.get_event_loop()
asyncio.ensure_future(getStarted(), loop = event_loop)