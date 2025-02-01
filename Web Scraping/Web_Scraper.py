import requests
from bs4 import BeautifulSoup
from pywinauto import Application
import time
import os
import threading

previous_urls = []  # List to store previous URLs
running = True  # Flag to control the auto scraping loop

def is_new_url(url):  # Function to check if URL is new
    if url not in previous_urls:
        previous_urls.append(url)
        return True
    else:
        return False

def get_url_with_protocol(url):  # Adds http:// to URL if needed
    if url.startswith("//"):
        return "http://" + url
    else:
        return "https://" + url

def write_to_file(data, filename, folder_name="Scraped_Data"):  # Writes data to document and stores in folder
    if not os.path.exists(folder_name):  # creates folder if folder does not exist
        os.makedirs(folder_name)

    filepath = os.path.join(folder_name, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)

def scrape_and_store():
    try:
        app = Application(backend='uia')  # Get URL from current open browser page
        try:
            app.connect(title_re=".*Chrome.*")
        except:
            print("No Browser open")
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

def auto_scrape():
    global running
    load_previous_urls()  # Load previous URLs
    while running:
        scrape_and_store()
        save_previous_urls()  # Save updated list after each run
        time.sleep(3)  # Set desired scraping interval (seconds)

def scrape_from_list(urls):
    for url in urls:
        url = get_url_with_protocol(url)
        if is_new_url(url):  # Check if URL is new
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "lxml")
                data_to_store = str(soup)

                safe_url = url.replace("http://", "").replace("https://", "").replace("/", "_")
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Generate timestamp for filename
                filename = f"{safe_url}_scraped_on_{timestamp}.txt"  # Adjust file type as needed

                write_to_file(data_to_store, filename)
                print(f"Scraped new URL: {url}")
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
        else:
            print(f"URL already scraped: {url}")

def load_previous_urls():  # Load previous URLs from a file
    filename = "previously_scraped_urls.txt"  # Adjust filetype as needed

    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                previous_urls.append(line.strip())

def save_previous_urls():  # Save previous URLs to a file
    filename = "previously_scraped_urls.txt"  # Adjust filetype as needed

    with open(filename, "w") as f:
        for url in previous_urls:
            f.write(url + "\n")

def main_menu():
    global running
    while True:
        print("Menu:\n"
              "1. Scrape sites in the background.\n"
              "2. Scrape a list of sites.\n"
              "3. Exit.\n")
        choice = input("Please select an option (1-3): \n")

        if choice == '1':
            running = True
            auto_scrape_thread = threading.Thread(target=auto_scrape)
            auto_scrape_thread.start()
            print("Auto scraping started. Press 'q' to stop.")

            while running:
                if input() == 'q':
                    running = False
                    print("Stopping auto scraping...")
                    auto_scrape_thread.join()  # Wait for the thread to finish
        
        elif choice == '2':
            print("Select input method:\n"
                  "1. Manually enter site names.\n"
                  "2. Use a file (e.g. Sites_to_scrape.txt).\n")
            input_method = input("Please select an option (1-2): \n")

            if input_method == '1':
                    urls_input = input("Enter a list of URLs separated by commas: \n")
                    urls = [url.strip() for url in urls_input.split(",")]
                    scrape_from_list(urls)
                    save_previous_urls()  # Save updated list after scraping
            
            elif input_method == '2':
                filename = input("Enter filename with sites to scrape: ")
                if os.path.exists(filename):
                    with open(filename, "r") as f:
                        urls = [line.strip() for line in f if line.strip()]  
                    scrape_from_list(urls)
                    save_previous_urls()  # Save updated list after scraping
                else:
                    print(f"File '{filename}' not found. Please create the file and add URLs.")
            
            else:
                print("Invalid choice. Please select a valid option.\n")
        
        elif choice == '3':
            print("Exiting the program.\n")
            running = False  # Ensure the auto scraping loop can exit
            break
        
        else:
            print("Invalid choice. Please select a valid option.\n")

if __name__ == "__main__":
    main_menu()