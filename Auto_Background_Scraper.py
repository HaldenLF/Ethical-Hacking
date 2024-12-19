import requests
from bs4 import BeautifulSoup
from pywinauto import Application
import time
import os


previous_urls = [] # Define list to store previous URLs

def is_new_url(url): # Function to check if URL is new
  if url not in previous_urls:
    previous_urls.append(url)
    return True
  else:
    return False
  

def get_url_with_protocol(url): # Adds http:// to URL
  if url.startswith("//"):
    return "http://" + url
  else:
    return "https://" + url
  

def write_to_file(data, filename, folder_name="Scraped_Data"): # Writes data to document and stores in folder

  if not os.path.exists(folder_name): # creates folder if not exist
    os.makedirs(folder_name)

  filepath = os.path.join(folder_name, filename)

  with open(filepath, "w", encoding="utf-8") as f:
    f.write(data)


def scrape_and_store():
  try:
      app = Application(backend='uia')  # Get URL from current open browser page
      # app.connect(title_re=".*Firefox.*")
      # element_name = "Search with Google or enter address"
      try:
        app.connect(title_re=".*Chrome.*")  # change browser as needed
      except:
        print("No Broswer open")
        return
      element_name = "Address and search bar"
      dlg = app.top_window()
      url = dlg.child_window(title=element_name, control_type="Edit").get_value()

      if url:  # Check if URL is not empty
          url = get_url_with_protocol(url)
          if is_new_url(url):  # Check if URL is new
              response = requests.get(url)
              soup = BeautifulSoup(response.text, "lxml")
              data_to_store = str(soup)

              safe_url = url.replace("http://", "").replace("https://", "").replace("/", "_")
              timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Generate timestamp for filename
              filename = f"{safe_url}_scraped_on_{timestamp}.txt"  # Adjust file type as needed

              write_to_file(data_to_store, filename)
              print(f"Scraped new URL: {url}")
          else:
              print(f"URL already scraped: {url}")
      else:
          print("No URL found")
          
  except Exception as e:
      print(f"Error: {str(e)}")


def load_previous_urls():# Load previous URLs from a file
  filename = "previous_urls.txt"  # Adjust filetype as needed

  if os.path.exists(filename):
    with open(filename, "r") as f:
      for line in f:
        previous_urls.append(line.strip())


def save_previous_urls(): # Save previous URLs to a file
  filename = "previous_urls.txt"  # Adjust filetype as needed

  with open(filename, "w") as f:
    for url in previous_urls:
      f.write(url + "\n")


if __name__ == "__main__":
  load_previous_urls()  # Load previous URLs

  while True:
    scrape_and_store()
    save_previous_urls() #Save updated list after each run
    time.sleep(3) # Set desired scraping interval (seconds)