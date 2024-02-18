from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup, Tag

from bluescraper.config import Config, TagScrapingConfig
from bluescraper.utils import TagDefinition, extract_from_tag
from bluescraper.validation import SoapValidator


class HtmlTagNotExists(Exception):
    pass


class NotValidHTML(Exception):
    pass


class Scraper:
    """
    A class for extracting information from beautifulsoup.
    """

    def __init__(self, soup: BeautifulSoup, config: Config) -> None:
        self.soup = soup
        self.config = config

    def can_scrape(self) -> bool:
        if self.config.validation:
            # TODO is this a case for apply dependency injection?
            validator = SoapValidator(
                soup=self.soup,
                validation_config=self.config.validation,
            )
            validator.validate()
            return validator.valid
        return True

    def extract_tag(
        self,
        soup: BeautifulSoup,
        tag: TagDefinition,
        content_type: Optional[str],
    ) -> str:
        page_elements = soup.find_all(name=tag.name, attrs=tag.attrs)
        if page_elements:
            extracted_content = [
                extract_from_tag(tag=page_element, attribute=content_type)
                for page_element in page_elements
                if isinstance(page_element, Tag)
            ]
            return self.concatenate_extracted_content(extracted_content)
        raise HtmlTagNotExists(
            f"No element found in html with name {tag.name} and attrs"
            f" {tag.attrs}"
        )

    def concatenate_extracted_content(
        self, content: List[str], delimiter="|"
    ) -> str:
        return delimiter.join(content)

    # TODO Find a better name as ScraperGroupData
    @dataclass
    class ScraperGroupData:
        results: List[dict]
        group_id: Optional[str] = None

    def extract(self) -> List[ScraperGroupData]:
        # TODO Simplify logic for the extraction
        if self.config.scraping.groups:
            return [
                Scraper.ScraperGroupData(
                    group_id=group.id,
                    results=[
                        {
                            tag.id: self.extract_tag(
                                soup=group_soup,
                                tag=tag.tag,
                                content_type=tag.content_type,
                            )
                            for tag in get_group_tags(
                                group.contains, self.config.scraping.tags
                            )
                        }
                        for group_soup in self.soup.find_all(
                            name=group.tag.name, attrs=group.tag.attrs
                        )
                    ],
                )
                for group in self.config.scraping.groups
            ]
        return [
            Scraper.ScraperGroupData(
                results=[
                    {
                        tag.id: self.extract_tag(
                            soup=self.soup,
                            tag=tag.tag,
                            content_type=tag.content_type,
                        )
                        for tag in self.config.scraping.tags
                    }
                ]
            )
        ]


def get_group_tags(
    contains: List[str], tags: List[TagScrapingConfig]
) -> List[TagScrapingConfig]:
    # TODO error handling
    return [tag for tag in tags if tag.id in contains]
