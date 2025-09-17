import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup


def scrape_website(website):
    """Scrape the full HTML of a given website using headless Chrome, including lazy-loaded content."""
    print(f"Scraping {website}...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(website)
        print("Page loaded.")

        # ✅ Wait until <body> is loaded before proceeding
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # ✅ Scroll until no new content loads (for lazy-loaded sites)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # wait for content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more content loaded
            last_height = new_height

        html = driver.page_source
        return html

    finally:
        driver.quit()
        print("Driver closed.")


def extract_body_content(html):
    """Extract only the <body> content from the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.body
    return str(body_content) if body_content else "No body content found."


def clean_body_content(body_content):
    """Remove scripts, styles, and empty lines from body content."""
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    clean_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in clean_content.splitlines() if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content, max_length=5000):
    """Split DOM content into chunks for LLM processing."""
    return [
        dom_content[i:i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]
