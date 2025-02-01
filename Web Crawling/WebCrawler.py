import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(url, filename):

  visited_urls = set()

  def visit(url):

    visited_urls.add(url)

    try:
      response = requests.get(url)
      if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = soup.find_all('a')

        with open(filename, 'a') as f:  # writes URL to file
          for link in all_links:
            href = link.get('href')
            absolute_url = urljoin(url, href)

            if absolute_url not in visited_urls and absolute_url.startswith(url): 
              visit(absolute_url) # checks if URL exists before adding
              f.write(f"  Found Link: {absolute_url}\n") 
      else:
        print("Error:", response.status_code)  # Print errors for debugging
    except requests.exceptions.RequestException as e:
      print("Error:", str(e))

  visit(url)

# Example usage:
crawl('https://www.webscraper.io', 'crawl_data.txt')
