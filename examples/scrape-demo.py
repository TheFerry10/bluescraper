import argparse
from pathlib import Path

from bluescraper import constants
from bluescraper.config import ConfigReader
from bluescraper.scraper import Scraper
from bluescraper.utils import get_soup


def scrape(url: str, date: str, category: str, config_path: str):
    soup = get_soup(
        url,
        request_params={"datum": date, "filter": category},
    )
    print(soup)
    config_reader = ConfigReader(Path(config_path))
    config = config_reader.load()
    scraper = Scraper(soup, config)
    return scraper.extract()


def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line interface example"
    )
    parser.add_argument(
        "--url",
        help="url",
        default="https://www.tagesschau.de/archiv?datum=2024-02-20&filter=inland",
        required=False,
    )
    parser.add_argument("--date", help="date", required=False)
    parser.add_argument("--category", help="category", required=False)
    parser.add_argument(
        "--config_path",
        help="category",
        default=constants.CONFIG_MULTIPLE_GROUPS_YAML,
        required=False,
    )
    args = parser.parse_args()
    result = scrape(
        url=args.url,
        date=args.date,
        category=args.category,
        config_path=args.config_path,
    )
    print(result)


if __name__ == "__main__":
    main()
