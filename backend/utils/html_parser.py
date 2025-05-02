from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:

    soup = BeautifulSoup(raw_html, 'html.parser')

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="")

    return " ".join(text.split())
