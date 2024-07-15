from bs4 import BeautifulSoup
import requests

def get_text_from_html(html_content: str):
    """
    Gets just the text of a HTML content

    Parameters:
    html_content (str): The HTML content itself

    Returns:
    str: The text.
    """

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.body.get_text().replace("\n", "")


if __name__ == "__main__":
    import sys
    print("Running module as test...")
    
    html_doc = requests.get(sys.argv[1]).text
    print(get_text_from_html(html_doc))
