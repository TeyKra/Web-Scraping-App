# Python Web Scraping Application

This Python project allows users to scrape websites and extract HTML data, with the option to log in, clean text of invisible characters, and export the extracted data to a CSV file. The project is built using `requests`, `BeautifulSoup`, `Selenium`, and `Rich` for an enhanced terminal user experience.

## Features

- **Web Scraping**: Scrapes HTML content from a specified URL using either `requests` or `Selenium` (for login-required pages).
- **Login Handling**: Automates logging in to websites that require authentication.
- **Data Extraction**: Extracts data from specified HTML tags, attributes, and classes.
- **Invisible Character Removal**: Optionally removes invisible Unicode characters from the scraped text.
- **CSV Export**: Exports the extracted data to a CSV file.
- **Interactive Console**: Uses the `Rich` library to create an interactive command-line interface for user input and data visualization.

## Requirements

- Python 3.6+
- `requests`
- `BeautifulSoup4`
- `selenium`
- `rich`
- `webdriver-manager`

Install the dependencies using:

```bash
pip install requests beautifulsoup4 selenium rich webdriver-manager
```

## Usage

Run the script and follow the prompts to scrape a website, with options for login, tag selection, and output format:

```bash
python main.py
```

### Step-by-Step Guide

1. **Enter the URL**: The script prompts for the website URL to scrape.
2. **Login Required?**: Indicate if login is required to access the page. If yes, enter the username and password.
3. **Remove Invisible Characters?**: Choose whether to clean the scraped text of invisible Unicode characters.
4. **Specify HTML Tags**: Optionally specify the HTML tag(s) to target during scraping (e.g., `p`, `div`, `h1`). If no tag is specified, all tags will be scraped.
5. **Optional Attribute**: If desired, specify an HTML attribute to extract (e.g., `href`, `src`).
6. **Export Data**: The extracted data will be displayed in a table and saved to a CSV file of your choice.

### Example Output

After scraping, the data is shown in a Rich table format:

```
+----+-------+--------------------------------+
| ID |  Tag  |         Content/Attribute      |
+----+-------+--------------------------------+
|  1 |  p    |  This is a paragraph.          |
|  2 |  a    |  Click here (URL: www.example.com) |
+----+-------+--------------------------------+
```

The data is also exported to a CSV file (`output.csv`).

### Sample Code

```python
# Example of extracting and cleaning HTML data
data = extract_data(soup, tag='p', class_name='content', remove_invisible=True)
export_to_csv(data, 'scraped_output.csv')
```

## Project Structure

```bash
main.py          # Main script for the web scraping application

```
