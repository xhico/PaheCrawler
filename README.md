# Pahe Link Scraping Tool

This is a Python script for Pahe Link scraping using Selenium. It is designed to navigate through download pages, detect whether they are in Single or Multi mode, and then click download buttons accordingly. It supports processing of specific pages like Intercelestial and Spacetica as well.

## Prerequisites

- Python 3.x
- Selenium
- Chrome WebDriver
- Chrome Browser (or any other browser supported by Selenium)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/xhico/PaheCrawler.git
    ```

2. Install dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

1. Navigate to the directory where the script is located.

2. Run the script with the URL of the download page as an argument:

    ```bash
    python3 PaheCrawler.py <download_page_url>
    ```

## Features

- Supports both Single and Multi mode download pages.
- Handles specific cases like Intercelestial and Spacetica pages.
- Saves scraped data to a JSON file for further analysis.

## Configuration

You may need to adjust certain parameters in the script according to your requirements:

- Chrome WebDriver path: Modify `Options.binary_location` in the script to specify the location of your Chrome browser executable.
- Logging settings: Logging configuration can be adjusted in the `main()` function according to your preferences.

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for efficient web scraping tools.
- Thanks to the Selenium and Python communities for their valuable contributions.
