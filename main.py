import gspread 
from google.oauth2.service_account import Credentials
from run import run
from undetected_playwright.sync_api import sync_playwright
scopes=[
    'https://www.googleapis.com/auth/spreadsheets'
]

creds= Credentials.from_service_account_file("credentials.json", scopes= scopes)
client= gspread.authorize(creds)

sheet_id= ""

sheet= client.open_by_key(sheet_id)

#list of all addresses
values_list= sheet.sheet1.col_values(9)
sqft_list=[]
counter= 1

for address in values_list[1:20]:
    with sync_playwright() as playwright:
        sqft= run(playwright, address)
        sqft_list.append(sqft)
        counter+=1
        sheet.sheet1.update_acell(f'T{counter}', f'{sqft}')






