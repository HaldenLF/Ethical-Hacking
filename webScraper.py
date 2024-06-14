import requests
from bs4 import BeautifulSoup

# Writes data to document
def write_to_file(data, filename):
    with open(filename, "w") as f:
        f.write(data)

# asks user for URL to scrape
userURL = input("What URL do you wish to scrape: \n"
                "> ")
response = requests.get(userURL)
soup = BeautifulSoup(response.text, "lxml")

# Stores the data in file
# can change file type to suit, e.g. .txt .pdf .docx .xlsx... etc.
data_to_store = str(soup)
filename = "data.pdf"

write_to_file(data_to_store, filename)