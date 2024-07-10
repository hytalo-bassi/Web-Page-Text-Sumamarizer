from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
from .nl_processing import *
from nltk import download
import time

# Configuração do WebDriver
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_page_text(url):
    driver.get(url)
    time.sleep(3)
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    return body_text


def main(urls: [str]):
    results = []
    
    if len(urls) == 0:
        print("No URLs")
        sys.exit()

    for url in urls:
        try:
            text = get_page_text(url)
            summary = generate_summary(text)
            relevant_terms = find_relevant_terms(text)
            results.append((url, summary, relevant_terms))
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    for result in results:
        print(f"URL: {result[0]}")
        print("Resumo:")
        print(result[1])
        print("Termos Relevantes:")
        for term, count in result[2]:
            print(f"- {term}: {count}")


if __name__ == "__main__":
    main(sys.argv[1:])

driver.quit()
