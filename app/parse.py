from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def parse_single_quote(quote_soup: BeautifulSoup) -> dict:
    tags = [tag.text for tag in quote_soup.select(".tag")]
    return dict(
        text=quote_soup.select_one(".text").text,
        author=quote_soup.select_one(".author").text,
        tags=tags
    )


def get_all_quotes() -> [dict]:
    quotes_list = []
    page_url = BASE_URL

    while page_url:
        page = requests.get(page_url).content
        soup = BeautifulSoup(page, "html.parser")

        quotes = soup.select(".quote")
        quotes_list.extend(
            [parse_single_quote(quote_soup) for quote_soup in quotes]
        )

        next_button = soup.select_one(".next > a")
        if next_button:
            next_page_url = next_button["href"]
            page_url = urljoin(BASE_URL, next_page_url)
        else:
            page_url = None
            print("It's done!")

    return quotes_list


def create_report(output_csv_path: str, quote_dict: dict) -> None:
    with open(output_csv_path, "a", encoding="utf-8") as file:
        file.write(
            f'{quote_dict["text"]},'
            f'{quote_dict["author"]},'
            f'{"|".join(quote_dict["tags"])}\n'
        )


def main(output_csv_path: str) -> None:
    all_quotes = get_all_quotes()
    for quote in all_quotes:
        create_report(output_csv_path, quote)


if __name__ == "__main__":
    main("quotes.csv")
