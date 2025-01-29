import requests
from bs4 import BeautifulSoup
import time
import os

# Define the base URL of the site (Hindi Wikipedia homepage)
base_url = "https://hi.wikipedia.org"

# Set to track visited URLs to avoid duplication
visited_urls = set()

# Directory to save scraped files
output_dir = "wikipedia_scraped_data"
os.makedirs(output_dir, exist_ok=True)

# Function to scrape a single page
def scrape_page(url, depth=0):
    if url in visited_urls or depth > 3:  # Stop if already visited or too deep
        return
    
    print(f"Scraping {url} at depth {depth}")
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Add the current URL to the visited set
    visited_urls.add(url)

    # Parse the content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title and text from the page
    title = soup.title.string if soup.title else "No Title"
    paragraphs = soup.find_all('p')

    # Create a filename based on the page title
    filename = os.path.join(output_dir, f"{title[:50]}.txt".replace("/", "-"))

    # Save the page content to a text file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")
        f.write(f"Title: {title}\n\n")
        for paragraph in paragraphs:
            text = paragraph.get_text()
            f.write(text + "\n")

    # Find all the links in the page to scrape recursively
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        if link.startswith('/wiki/') and not ':' in link:  # Only internal Wikipedia article links
            full_link = base_url + link
            scrape_page(full_link, depth + 1)  # Recursive call to scrape next link

    # Throttle the requests to avoid overloading the server
    time.sleep(1)

# Start scraping from the homepage
scrape_page(base_url + "/wiki/%E0%A4%AE%E0%A5%81%E0%A4%96%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0")
