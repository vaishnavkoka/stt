import os
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import random
import concurrent.futures

# Initialize Pandas DataFrame to store URLs and filenames
data = pd.DataFrame(columns=["URL", "File Name"])

# Initialize total data size
total_data_size = 0
max_data_size = 1 * 1024 * 1024  # 1GB in bytes
all_urls = set()

# Store the original directory before changing it
original_directory = os.getcwd()

# Function to check if content is primarily Hindi
def is_hindi(text):
    hindi_chars = re.findall(r'[\u0900-\u097F]', text)
    return len(hindi_chars) / len(text) if len(text) > 0 else 0

# Function to get all <p> tag content and clean text
def get_clean_text(soup):
    paragraphs = soup.find_all('p')
    text = ""
    for paragraph in paragraphs:
        temp = paragraph.get_text()
        if is_hindi(temp) > 0.6:
            text += temp
    return text

# Function to check if URL belongs to Wikipedia
def is_wikipedia_url(url):
    return "wikipedia.org" in url

# Function to get all URLs on the page
def get_all_urls(soup):
    urls = []
    links = soup.find_all('a', href=True)
    for link in links:
        url = link['href']
        if url.startswith('http'):  # Ensure valid URLs
            urls.append(url)
    return set(urls)

# Main scraping function
def scrape_page(url, directory):
    global total_data_size
    global all_urls
    all_urls.add(url)
    print("Scraping URL:", url, end=": ")

    try:
        # Send GET request and parse with BeautifulSoup
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get clean Hindi content
        text = get_clean_text(soup)
        
        # Check Hindi content percentage
        hindi_percentage = is_hindi(text)
        
        if len(text) > 500 and hindi_percentage > 0.5:
            file_name = f"{directory}/page_content_{len(data)}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(text)
                data_size = os.path.getsize(file_name)
                total_data_size += data_size
                print(f"Stored {file_name}, size: {data_size} bytes")
            
            # Add entry to the dataframe
            data.loc[len(data)] = [url, file_name]

            # Stop if total data size exceeds 1GB
            if total_data_size >= max_data_size:
                print("Reached 1GB of stored data. Stopping...")
                return False
        
        if hindi_percentage > 0.1:
            # Extract all URLs and scrape them recursively
            new_urls = list(get_all_urls(soup))
            random.shuffle(new_urls)
            if total_data_size < max_data_size:
                for new_url in new_urls:
                    if new_url not in all_urls:
                        scrape_page(new_url, directory)
            else:
                return False
        else:
            print('Skipped (low Hindi content)')
    
    except (requests.RequestException, Exception) as e:
        print(f"Error with URL {url}: {e}")
        return False
    
    return True

# List of URLs to scrape
urls = [
    "https://www.livehindustan.com/bihar/patna/story-bjp-spokesperson-criticizes-rahul-gandhi-s-comments-on-kashmir-and-outsiders-201725801344063.html"
]

# Create a directory for saving data
directory = str(int(time.time()))
print(directory)
os.mkdir(directory)
os.chdir(directory)

# Use ThreadPoolExecutor to run scraping tasks concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
    for i in range(len(urls)):
        os.mkdir(str(i))
    future_to_url = {executor.submit(scrape_page, url, str(i)): url for i,url in enumerate(urls)}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result()
        except Exception as e:
            print(f"Error scraping {url}: {e}")

# Change back to the original directory to save the CSV
os.chdir(original_directory)
data.to_csv(f"{directory}/scraped_data_log.csv", index=False)

print("Scraping completed.")
