from flask import Flask, request, render_template, redirect, url_for
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def scrape_text(soup, txt_file):
    with open(txt_file, 'w') as file:
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.get_text(strip=True)
            if text:
                file.write(text + "\n")

def scrape_links(soup, txt_file):
    with open(txt_file, 'w') as file:
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            file.write(full_url + "\n")

def scrape_files(soup, file_types, folder, tag_attr):
    os.makedirs(folder, exist_ok=True)
    for file_type in file_types:
        for tag in soup.find_all(src=True):
            if tag[tag_attr].lower().endswith(file_type):
                file_url = urljoin(url, tag[tag_attr])
                file_name = os.path.basename(file_url)
                save_path = os.path.join(folder, file_name)
                download_file(file_url, save_path)

def scrape_website(url, file_types, options, folders):
    try:
        response = requests.get(url)
        response.raise_for_status()
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

        return True

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html', success=None)

@app.route('/scrape', methods=['POST'])
def scrape():
    global url
    url = request.form['url']
    file_types = {
        'images': ['.png', '.jpeg', '.jpg', '.gif'],
        'videos': ['.mp4', '.avi', '.mov'],
        'audio': ['.mp3', '.wav'],
        'documents': ['.pdf', '.docx', '.xlsx']
    }
    
    selected_options = []
    if 'text' in request.form:
        selected_options.append('text')
    if 'links' in request.form:
        selected_options.append('links')
    if 'images' in request.form:
        selected_options.append('images')
    if 'videos' in request.form:
        selected_options.append('videos')
    if 'audio' in request.form:
        selected_options.append('audio')
    if 'documents' in request.form:
        selected_options.append('documents')

    folders = {}
    if 'text' in selected_options:
        folders['text'] = request.form['text_folder']
    if 'links' in selected_options:
        folders['links'] = request.form['links_folder']
    if 'images' in selected_options:
        folders['images'] = request.form['images_folder']
    if 'videos' in selected_options:
        folders['videos'] = request.form['videos_folder']
    if 'audio' in selected_options:
        folders['audio'] = request.form['audio_folder']
    if 'documents' in selected_options:
        folders['documents'] = request.form['documents_folder']

    success = scrape_website(url, file_types, selected_options, folders)
    return render_template('index.html', success=success)

if __name__ == '__main__':
    app.run(debug=True)
