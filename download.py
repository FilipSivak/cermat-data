from bs4 import BeautifulSoup
import requests
import os
import io
import pandas as pd
from datetime import datetime
from tqdm import tqdm

CERMAT_URL = "https://vysledky.cermat.cz/data/Default.aspx"

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

def get_option_values(selector):
    return [option["value"] for option in soup.select(selector) if option["value"] != "X"]

def request_data(soup, year, region, course, exam):
    fname = f"backup_{year}_{region}_{course}_{exam}.html"
    
    content = None
    if not os.path.exists(fname):
        url = CERMAT_URL
        payload = {
            "__EVENTTARGET": "upParametry",
            "__EVENTARGUMENT": "DZ",
            "__VIEWSTATE": soup.select("#__VIEWSTATE")[0]["value"],
            "__VIEWSTATEGENERATOR": soup.select("#__VIEWSTATEGENERATOR")[0]["value"],
            "__VIEWSTATEENCRYPTED": soup.select("#__VIEWSTATEENCRYPTED")[0]["value"],
            "__EVENTVALIDATION": soup.select("#__EVENTVALIDATION")[0]["value"],
            "ctl00$LeftContent$ddRok": year,
            "ctl00$LeftContent$ddKraj": region,
            "ctl00$LeftContent$ddPredmet": course,
            "ctl00$LeftContent$ddDilciZkouska": exam
        }
        req = requests.post(url, data=payload, headers = headers)
        with io.open(fname, mode = "w", encoding="utf8") as f:
            f.write(req.text)
        content = req.text
    else:
        with io.open(fname, mode = "r", encoding="utf8") as f:
            content = f.read()

    excel_name =  f"cermat_maturita_{year}_{region}_{course}_{exam}.xlsx"
    return store_table_as_excel(excel_name, content)

def store_table_as_excel(file_name, page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    rows = soup.select("#table tr")

    header = ["REDIZO", "Název školy", "Kraj"]
    for cell in rows[1].select("th"):
        header.append(cell.text.strip())

    data = []
    for row in rows[2:]:
        row_data = []
        cells = row.select("td")

        # Skip aggregations at the top of the table
        if len(cells) < 20:
            continue

        for cell in cells[1:]:
            row_data.append(cell.text)
        data.append(row_data)

    df = pd.DataFrame(data, columns = header)
    df.to_excel(file_name, index = False)
    return df

req = requests.get(CERMAT_URL, headers)
soup = BeautifulSoup(req.content, 'html.parser')

years = get_option_values("#ddRok option")
regions = get_option_values("#ddKraj option")
courses = get_option_values("#ddPredmet option")
exams = get_option_values("#ddDilciZkouska option") 

iterations = []
for year in years:
    for region in regions:
        for course in courses:
            for exam in exams:
                iterations.append((year, region, course, exam))

dataframes = []
for  year, region, course, exam in tqdm(iterations):
    df = request_data(soup, year, region, course, exam)
    df["Rok"] = year
    df["Předmět"] = course
    df["Dílčí zkouška"] = exam
    dataframes.append(df)

final_filename = f"maturita_{datetime.today().strftime('%d-%m-%Y')}.xlsx"
final_df = pd.concat(dataframes)
final_df.to_excel(final_filename, index = False)
print(f"Collected {len(dataframes)} dataframes with {len(final_df.index)} rows and joined them into {final_filename}.")
