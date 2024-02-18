import datetime

import pytest
from bs4 import BeautifulSoup

from bluescraper.config import ConfigReader
from bluescraper.scraper import Scraper


@pytest.fixture(name="html")
def html_(request):
    file_path = request.param
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture(name="soup")
def soup_(html):
    return BeautifulSoup(html, "html.parser")


@pytest.fixture(name="config")
def config_(request):
    config_path = request.param
    config_reader = ConfigReader(config_path)
    return config_reader.load()


@pytest.fixture(name="scraper")
def scraper_(soup, config):
    return Scraper(soup, config)


@pytest.fixture(name="request_params")
def request_params_():
    date_ = datetime.date(2023, 11, 4)
    category = "wirtschaft"
    archive_filter = ArchiveFilter(date_, category)
    return create_request_params(archive_filter)
