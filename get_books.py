import re
import requests
from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup


BASE_URL = "https://link.springer.com"


def get_raw(location):
    return requests.get(location, stream=True)


def make_soup(location):
    page = get_raw(location)
    _html = BytesIO()
    _html.write(page.content)
    return BeautifulSoup(_html.getvalue(), "html.parser")


def save_book(url, title):
    folder = Path.home().joinpath("Downloads")
    assert folder.exists()
    location = folder.joinpath(title)
    print(f"url: {url}")
    book = get_raw(url)
    with open(f"{location}", "wb") as _file:
        for chunk in book.iter_content(chunk_size=512):
            _file.write(chunk)
    print(f"saving <{title}> to: {location}\n")


def book_links():
    soup = make_soup(
        "https://towardsdatascience.com/springer-has-released-65-machine-learning-and-data-books-for-free-961f8181f189"
    )
    anchor_tags = soup.find_all(href=re.compile("^http://link.springer.com/openurl"))
    print(len(anchor_tags))
    return (tag.contents[0] for tag in anchor_tags)


def download_books():
    for link in book_links():
        soup = make_soup(link)
        _title = soup.find_all("h1")[0].contents[0].replace(" ", "_")
        book_title = f"2020_{_title}.pdf"
        download_button = soup.find(attrs={"class": "test-bookpdf-link"})
        if download_button is not None:
            download_url = download_button.attrs["href"]
            book_url = f"{BASE_URL}{download_url}"
            save_book(book_url, book_title)


if __name__ == "__main__":
    print(f"Downloading free books from {BASE_URL}\n")
    download_books()
