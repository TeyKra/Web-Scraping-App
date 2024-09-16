import re
import requests
from bs4 import BeautifulSoup
import csv
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

console = Console()

# Function to clean invisible characters
def clean_text(text, remove_invisible=False):
    if remove_invisible:
        return re.sub(r'[^\x20-\x7E]', '', text)  # Remove invisible Unicode characters
    return text

# Step 1: Fetch the HTML page using requests or Selenium, depending on whether login is required
def fetch_page(url, requires_login=False, username=None, password=None):
    if requires_login:
        console.log("[yellow]Login required. Using Selenium to log in...[/yellow]")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")  # Run without GUI

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the login page
        driver.get("https://www.linkedin.com/login")
        sleep(2)

        # Enter username and password, and log in
        driver.find_element(By.NAME, "session_key").send_keys(username)
        driver.find_element(By.NAME, "session_password").send_keys(password)
        driver.find_element(By.NAME, "session_password").send_keys(Keys.RETURN)

        sleep(5)
        # Navigate to the target URL after logging in
        driver.get(url)
        sleep(5)

        # Get the page source
        html_content = driver.page_source
        driver.quit()
        return html_content
    else:
        try:
            # Fetch the page using requests if no login is required
            response = requests.get(url)
            if response.status_code == 200:
                console.log(f"[green]Page successfully fetched: {url}[/green]")
                return response.text
            else:
                console.log(f"[red]Error fetching the page: {response.status_code}[/red]")
                return None
        except Exception as e:
            console.log(f"[red]Error fetching the page: {e}[/red]")
            return None

# Step 2: Parse the HTML page using BeautifulSoup
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Step 3: Extract data from HTML tags, CSS classes, or all elements
def extract_data(soup, tag=None, class_name=None, attribute=None, remove_invisible=False):
    if tag:
        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)
    else:
        elements = soup.find_all(True)  # Capture all tags

    data = []
    for element in elements:
        if attribute:
            value = element.get(attribute)
            if value:
                data.append([element.name, clean_text(value, remove_invisible)])  # Clean the attribute value
        else:
            content = clean_text(element.get_text().strip(), remove_invisible)
            if content:
                data.append([element.name, content])  # Capture the tag text

        # Capture specific tags like <pre>, <code>, and <a> links
        if element.name == "pre":
            pre_content = clean_text(element.get_text().strip(), remove_invisible)
            data.append([element.name, pre_content])

        if element.name == "code":
            code_content = clean_text(element.get_text().strip(), remove_invisible)
            data.append([element.name, code_content])

        if element.name == "a" and element.get('href'):
            link_text = clean_text(element.get_text().strip(), remove_invisible)
            link_url = clean_text(element['href'], remove_invisible)
            data.append([element.name, f'{link_text} (URL: {link_url})'])

    return data

# Step 4: Export the extracted data to a CSV file
def export_to_csv(data, filename="output.csv"):
    if not filename.endswith(".csv"):
        filename += ".csv"
    
    # Write data to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Content/Attribute"])
        for row in data:
            writer.writerow(row)
    console.log(f"[green]Data exported to {filename}[/green]")

# Main function to orchestrate the scraping process
def scrape_website(url, requires_login=False, username=None, password=None, tag=None, class_name=None, attribute=None, remove_invisible=False, output_file="output.csv"):
    html_content = fetch_page(url, requires_login, username, password)
    if html_content:
        soup = parse_html(html_content)
        data = extract_data(soup, tag, class_name, attribute, remove_invisible)
        
        if data:
            table = Table(title="Extracted Data")
            table.add_column("Tag", justify="right", style="cyan", no_wrap=True)
            table.add_column("Content/Attribute", style="magenta")
            
            # Display the extracted data in a Rich table
            for idx, row in enumerate(data, start=1):
                table.add_row(str(idx), row[0], row[1])
                
            console.print(table)
            
            with Progress() as progress:
                task = progress.add_task("[green]Exporting data...", total=len(data))
                export_to_csv(data, output_file)
                progress.update(task, advance=len(data))
        else:
            console.log("[yellow]No data was extracted.[/yellow]")
    else:
        console.log("[red]Unable to fetch the page content.[/red]")

# User interface with Rich for interactive input
def main():
    console.print("[bold magenta]Welcome to the Python Web Scraping Application[/bold magenta] :snake:")

    url = Prompt.ask("[cyan]Enter the URL of the website to scrape[/cyan]")
    
    requires_login = Prompt.ask("[cyan]Does this page require a login (yes/no)?[/cyan]", default="no").lower() == "yes"
    
    username = None
    password = None
    if requires_login:
        username = Prompt.ask("[cyan]Enter your username or email for login[/cyan]")
        password = Prompt.ask("[cyan]Enter your password[/cyan]", password=True)

    # Option to enable or disable the removal of invisible characters
    remove_invisible = Prompt.ask("[cyan]Do you want to remove invisible characters (yes/no)?[/cyan]", default="no").lower() == "yes"
    
    tag = Prompt.ask("[cyan]Enter the HTML tag to scrape (e.g., p, div, h1) or leave blank to scrape all elements[/cyan]", default="")
    
    class_name = Prompt.ask("[cyan]Enter the CSS class (optional, press enter to skip)[/cyan]", default="")
    
    attribute = Prompt.ask("[cyan]Enter the attribute to extract (optional, e.g., href, src, press enter to skip)[/cyan]", default="")
    
    output_file = Prompt.ask("[cyan]Enter the name of the output file (e.g., output.csv)[/cyan]", default="output.csv")

    scrape_website(url, requires_login, username, password, tag if tag else None, class_name if class_name else None, attribute if attribute else None, remove_invisible, output_file)

if __name__ == "__main__":
    main()
