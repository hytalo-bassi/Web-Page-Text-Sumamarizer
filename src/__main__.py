import requests
import sys
from .nl_processing import *
from .html_processing import get_text_from_html
from nltk import download


def get_page_text(driver, url):
    import time
    
    driver.get(url)
    time.sleep(3) # Wait for selenium to load
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    
    return body_text


def import_selenium():
    print("Using selenium is really buggy now. Ensure that chrome or chromium is installed!")

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = Options()
    options.headless = True
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def main(urls: [str]):
    driver = None
    results = []
    
    if len(urls) == 0:
        print("No URLs")
        sys.exit()
    
    val = input('Use selenium [y/N]: ').lower()
    use_selenium = True
    if val == 'n' or val == '':
        use_selenium = False

    for url in urls:
        try:
            text = None
            if use_selenium:
                driver = import_selenium()
                text = get_page_text(driver, url)
            else:
                text = get_text_from_html(requests.get(url).text)
            summary = generate_summary(text)
            relevant_terms = find_relevant_terms(text)
            results.append((url, summary, relevant_terms))
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    if use_selenium:
        driver.quit()

    for result in results:
        print(f"URL: {result[0]}")
        print("Resumo:")
        print(result[1])
        print("Termos Relevantes:")
        for term, count in result[2]:
            print(f"- {term}: {count}")
    

if __name__ == "__main__":
    main(sys.argv[1:])

