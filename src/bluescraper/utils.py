import datetime
import hashlib
from typing import Callable, Dict, Optional, Union

import requests
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from bluescraper.constants import DEFAULT_TIMEOUT


def get_extraction_timestamp() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()


class TagDefinition(BaseModel):
    name: Optional[str] = None
    attrs: Optional[Dict[str, Union[str, int, bool]]] = None


def is_tag_in_soup(soup: BeautifulSoup, tag_definition: TagDefinition) -> bool:
    if soup.find(name=tag_definition.name, attrs=tag_definition.attrs):
        return True
    return False


def is_text_in_tag(
    soup: BeautifulSoup,
    tag_definition: TagDefinition,
    text: str,
) -> bool:
    tag = soup.find(tag_definition.name, tag_definition.attrs)
    if tag:
        return text in tag.get_text(strip=True)
    return False


def clean_string(string: str):
    return " ".join([word.strip() for word in string.split()])


def extract_text(tag: Tag) -> str:
    text = tag.get_text()
    return clean_string(text)


class HtmlAttributeNotExists(Exception):
    pass


def extract_from_tag(
    tag: Tag,
    attribute: Optional[str] = None,
    formatter: Callable[[str], str] = clean_string,
) -> str:
    if attribute:
        try:
            text = tag[attribute]
        except KeyError as e:
            raise HtmlAttributeNotExists(
                f"Attribute {attribute} not exists in html element"
            ) from e
    else:
        text = extract_text(tag)
    return formatter(text)


def transform_date_to_date_in_headline(date_: datetime.date) -> str:
    year = date_.year
    month = date_.month
    day = date_.day
    return f"{day}. {constants.GERMAN_MONTHS[month]} {year}"


def transform_date_in_headline_to_date(date_in_headline: str) -> datetime.date:
    day_raw, month_raw, year_raw = date_in_headline.split()
    day = int(day_raw[:-1])
    month = constants.GERMAN_MONTHS.index(month_raw)
    year = int(year_raw)
    return datetime.date(year, month, day)


def cast_to_list(input_: object) -> list[object]:
    if not isinstance(input_, list):
        return [input_]
    return input_


def transform_datetime_str(datetime_string: str) -> str:
    """
    Transform datetime string to "%Y-%m-%d %H:%M:00".

    Parameters
    ----------
    datetime_string : str
        Provided datetime string.

    Returns
    -------
    str
        Transformed datetime string

    Examples
    --------
    transform_datetime_str("30.01.2021 - 18:04 Uhr")
    >>> 2021-01-30 18:04:00
    transform_datetime_str("30.01.2021 -    20:04 Uhr")
    >>> 2021-01-30 20:04:00
    """
    date_, time = [x.strip() for x in datetime_string.split("-")]
    day, month, year = date_.split(".")
    hour, minute = time.split(" ")[0].split(":")
    second = "00"
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def get_hash_from_string(string: str) -> str:
    result = hashlib.sha1(string.encode())
    return result.hexdigest()


def get_date_range(
    start_date: datetime.date, end_date: datetime.date
) -> list[datetime.date]:
    """
    Return a date range from start date (inclusive) to end date (exclusive)
    with an interval of 1 day.

    Parameters
    ----------
    start_date : date
        Start date (inclusive)
    end_date : date
        End date (exclusive)

    Returns
    -------
    list[date]
        List of dates

    Raises
    ------
    ValueError
        When end_date is before start_date
    """
    if end_date > start_date:
        days_between = (end_date - start_date).days
        return [
            start_date + datetime.timedelta(days=days)
            for days in range(days_between)
        ]
    else:
        raise ValueError("end_date must be after start_date.")


def get_html(url: str, request_params: Optional[dict] = None) -> str:
    response = requests.get(
        url=url, params=request_params, timeout=DEFAULT_TIMEOUT
    )
    if response.ok:
        return response.text
    raise ValueError


def get_soup(url: str, request_params: Optional[dict] = None) -> BeautifulSoup:
    html = get_html(url, request_params)
    return BeautifulSoup(html, "html.parser")
