import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_text(soup, txt_file):
    print("\nScraping Text Content...")
    with open(txt_file, 'w') as file:
        for tag in soup.find_all(['p', 'h1', 'h2', 'div']):
            text = tag.get_text(strip=True)
            print(text)
            file.write(text + "\n")

def scrape_links(soup, txt_file):
    print("\nScraping Links...")
    with open(txt_file, 'w') as file:
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            print(full_url)
            file.write(full_url + "\n")

def scrape_files(soup, file_types, folder, tag_attr):
    print(f"\nScraping Files in {folder}...")
    os.makedirs(folder, exist_ok=True)
    for file_type in file_types:
        for tag in soup.find_all(src=True):
            if tag[tag_attr].endswith(file_type):
                file_url = urljoin(url, tag[tag_attr])
                file_name = os.path.basename(file_url)
                save_path = os.path.join(folder, file_name)
                download_file(file_url, save_path)

def scrape_website(url, file_types, options, folders):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'text' in options:
            text_file = os.path.join(folders['text'], 'scraped_content.txt')
            scrape_text(soup, text_file)
        if 'links' in options:
            links_file = os.path.join(folders['links'], 'links.txt')
            scrape_links(soup, links_file)
        if 'images' in options:
            scrape_files(soup, file_types['images'], folders['images'], 'src')
        if 'videos' in options:
            scrape_files(soup, file_types['videos'], folders['videos'], 'src')
        if 'audio' in options:
            scrape_files(soup, file_types['audio'], folders['audio'], 'src')
        if 'documents' in options:
            scrape_files(soup, file_types['documents'], folders['documents'], 'src')

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

if __name__ == "__main__":
    # Get user input from the terminal
    url = input("Enter the website URL: ").strip()
    if not url:
        print("URL cannot be empty.")
        exit()

    # Define available options
    options = {
        '1': 'text',
        '2': 'links',
        '3': 'images',
        '4': 'videos',
        '5': 'audio',
        '6': 'documents'
    }

    # Display options
    print("\nSelect what to scrape:")
    for number, description in options.items():
        print(f"{number}: {description}")

    # Get user selection
    selected_numbers = input("Enter the numbers of the options you want to enable (comma-separated): ").strip()
    if not selected_numbers:
        print("No options selected.")
        exit()
        
    selected_options = [options[num.strip()] for num in selected_numbers.split(',') if num.strip() in options]
    if not selected_options:
        print("Invalid options selected.")
        exit()

    # Define file types for different categories
    file_types = {
        'images': ['.png', '.jpeg', '.jpg', '.gif'],
        'videos': ['.mp4', '.avi', '.mov'],
        'audio': ['.mp3', '.wav'],
        'documents': ['.pdf', '.docx', '.xlsx']
    }

    # Initialize folders
    folders = {}

    # Get folder names based on selected options
    if 'text' in selected_options:
        text_folder = input("Enter the folder name to save text files: ").strip()
        if not text_folder:
            print("Folder name for text files cannot be empty.")
            exit()
        folders['text'] = text_folder

    if 'links' in selected_options:
        links_folder = input("Enter the folder name to save links files: ").strip()
        if not links_folder:
            print("Folder name for links files cannot be empty.")
            exit()
        folders['links'] = links_folder

    if 'images' in selected_options:
        images_folder = input("Enter the folder name to save image files: ").strip()
        if not images_folder:
            print("Folder name for image files cannot be empty.")
            exit()
        folders['images'] = images_folder

    if 'videos' in selected_options:
        videos_folder = input("Enter the folder name to save video files: ").strip()
        if not videos_folder:
            print("Folder name for video files cannot be empty.")
            exit()
        folders['videos'] = videos_folder

    if 'audio' in selected_options:
        audio_folder = input("Enter the folder name to save audio files: ").strip()
        if not audio_folder:
            print("Folder name for audio files cannot be empty.")
            exit()
        folders['audio'] = audio_folder

    if 'documents' in selected_options:
        documents_folder = input("Enter the folder name to save document files: ").strip()
        if not documents_folder:
            print("Folder name for document files cannot be empty.")
            exit()
        folders['documents'] = documents_folder

    # Start the scraping process
    scrape_website(url, file_types, selected_options, folders)
