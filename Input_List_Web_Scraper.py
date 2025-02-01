import requests
import time
import os
from bs4 import BeautifulSoup

previous_urls = [] # Define list to store previous URLs

def is_new_url(url): # Function to check if URL is new
  if url not in previous_urls:
    previous_urls.append(url)
    return True
  else:
    return False 

def write_to_file(data, filename, folder_name="Scraped_Data"): # Writes data to document and stores in folder

  if not os.path.exists(folder_name): # creates folder if not exist
    os.makedirs(folder_name)

  filepath = os.path.join(folder_name, filename)

  with open(filepath, "w", encoding="utf-8") as f:
    f.write(data)

def read_urls(filename):
  with open(filename, 'r') as f:
      urls = [line.strip() for line in f]  # Strip trailing whitespace
  return urls

def scrape_and_store():
  urls = read_urls("Sites_to_scrape.txt") # change to filename of list of sites to be scraped
  new_urls_scraped = False

  for url in urls:
      if is_new_url(url): # Check if URL is new
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        data_to_store = str(soup)

        safe_url = url.replace("http://", "").replace("https://", "").replace("/", "_")
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S") # Generate timestamp for filename
        filename = f"{safe_url}_scraped_on_{timestamp}.txt"  # Adjust file type as needed

        write_to_file(data_to_store, filename)
        print(f"Scraped new URL: {url}")
      else:
        print(f"URL already scraped: {url}")

  return new_urls_scraped

def load_previous_urls():# Load previous URLs from a file
  filename = "previous_scraped_urls.txt"  # Adjust filetype as needed

  if os.path.exists(filename):
    with open(filename, "r") as f:
      for line in f:
        previous_urls.append(line.strip())


def save_previous_urls(): # Save previous URLs to a file
  filename = "previous_scraped_urls.txt"  # Adjust filetype as needed

  with open(filename, "w") as f:
    for url in previous_urls:
      f.write(url + "\n")


if __name__ == "__main__":
  load_previous_urls()  # Load previous URLs

  while True:
    new_urls_scraped = scrape_and_store()
    save_previous_urls() #Save updated list after each run

    if not new_urls_scraped:
      break