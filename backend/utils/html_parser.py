from bs4 import BeautifulSoup


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "svg", "form", "input", "button", "aside"]):
        tag.decompose()

    # Remove elements that are hidden
    for tag in soup.select('[style*="display:none"], [style*="visibility:hidden"], [hidden]'):
        tag.decompose()

    # Extract text with reasonable line breaks
    text = soup.get_text(separator="\n")

    # Drop short/low-content lines and extra whitespace
    cleaned_lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 40]
    return " ".join(cleaned_lines)
