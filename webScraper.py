
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from pywinauto import Application
import time

# Adds http:// to URL from current open browser page
def get_url_with_protocol(chrome_url):
  if chrome_url.startswith("//"):
    return "http://" + chrome_url
  else:
    return "https://" + chrome_url
  
# Writes data to document
def write_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

def scrape_and_store(): 
    app = Application(backend='uia')

    app.connect(title_re=".*Chrome.*")

    element_name="Address and search bar"

    dlg = app.top_window()

    url = get_url_with_protocol(dlg.child_window(title=element_name, control_type="Edit").get_value())

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    data_to_store = str(soup)

    # Generate timestamp for filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{timestamp}.pdf"  # Adjust file type as needed

    write_to_file(data_to_store, filename)

scrape_and_store()

#  Simpler version that takes user input
# ----------------------------------------------------------------------------------
# 
# 
# import requests
# from bs4 import BeautifulSoup

# # Writes data to document
# def write_to_file(data, filename):
#     with open(filename, "w") as f:
#         f.write(data)

# # asks user for URL to scrape
# userURL = input("What URL do you wish to scrape (https://example.com): \n"
#                 "> ")
# response = requests.get(userURL)
# soup = BeautifulSoup(response.text, "lxml")

# # Stores the data in file
# # can change file type to suit, e.g. .txt .pdf .docx .xlsx... etc.
# data_to_store = str(soup)
# filename = "data.pdf"

# write_to_file(data_to_store, filename)