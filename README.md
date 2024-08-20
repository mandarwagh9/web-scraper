# Web Scraper

## Overview

This project is a Flask-based web application designed to scrape various types of content from a specified URL. It allows users to extract text, links, images, videos, audio files, and documents from a webpage and save them to designated folders.

## Features

- Scrapes text from `<p>` and header tags (`<h1>`, `<h2>`, etc.)
- Extracts all hyperlinks from the page
- Downloads images, videos, audio files, and documents based on user selection
- Saves scraped content to specified folders
- Provides a user-friendly interface for scraping configuration

## Setup

### Prerequisites

- Python 3.x
- Flask
- Requests
- BeautifulSoup4

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mandarwagh/web-scraper
    cd web-scraper
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Open your web browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```

3. **Use the form to specify the URL and choose the types of content you want to scrape.** You can select:
   - Text
   - Links
   - Images
   - Videos
   - Audio
   - Documents

4. **Specify the folders where you want to save each type of content.** For optional fields, leave them blank if you don't want to save that type of content.

5. **Click the "Start Scraping" button to begin the scraping process.** A popup will appear to notify you when the scraping is complete.

## DEMO

![DEMO](https://github.com/mandarwagh9/web-scraper/blob/main/webscraper.PNG?raw=true)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you need any additional information or modifications!
