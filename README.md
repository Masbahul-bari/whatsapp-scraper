# WhatsApp Channel Scraper

This project is a Python-based web scraper for WhatsApp Web channels. It uses Selenium to automate browser actions and extract messages, images, reactions number, and other post data from WhatsApp channels.

## Features
- Login to WhatsApp Web using session or QR code
- Navigate and search for specific channels
- Scrape post text, images, post time, and number of reactions
- Save each channel's posts as a separate JSON file
- Download images from posts

## Requirements
- Python 3.8+
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)
- [Selenium](https://pypi.org/project/selenium/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/whatsapp-scraper.git
   cd whatsapp-scraper
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download ChromeDriver:(if needed)**
   - Download the version matching your Chrome browser from [here](https://chromedriver.chromium.org/downloads).
   - Place it in your PATH or project directory.

## Usage
1. **Run the script:**
   ```bash
   python main.py
   ```
2. **Login:**
   - The script will try to use session for login. If not present, scan the QR code in the opened browser window.
3. **Scraping:**
   - The script will search for channels, scrape posts, download images, and save data as JSON files in the `channel_jsons/` folder.

## Important Notes

- **You must follow the channels you want to scrape.**
  - The script will only work for channels you have already followed in your WhatsApp account.
- **Update the `Channels` list in `main.py`:**
  - Edit the `Channels` variable (see line 272) to include the links of the channels you want to scrape.
- **Set your Chrome profile path:**
  - Make sure the `chrome_profile_path` variable (see line 276) matches your Chrome user profile directory. This allows the script to use your existing WhatsApp session.

  - Make sure to keep your Chrome browser and ChromeDriver up to date.
  - Respect WhatsApp's terms of service and privacy policies.
