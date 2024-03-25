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
        """
        Extract the text information from a tag when it exists within the soup
        object.
        The content_type parameter specifies the html attribute from with the
        text should be read, when not set, the text will be retrieved from the
        text of the html element. In case of multiple occurrences of the same
        tag, the results of each extraction will be concatenated.

        Args:
            soup (BeautifulSoup): Soup for searching occurrences
            tag (TagDefinition): The target page element
            content_type (Optional[str]): When specified, the target attribute
            to extract within the page element

        Raises:
            HtmlTagNotExists: No match found of the page element within the soup

        Returns:
            str: Extracted page element in soup. Can be also a concatenated
            string for multiple occurrences.
        """
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

    def get_group_soups(
        self, soup: BeautifulSoup, tag: TagDefinition
    ) -> Optional[List[BeautifulSoup]]:
        group_soups = soup.find_all(tag.name, attrs=tag.attrs)
        if group_soups:
            return group_soups
        raise HtmlTagNotExists(
            f"No element found in html with name {tag.name} and attrs"
            f" {tag.attrs}"
        )

    def extract_by_group(self):
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
                    for group_soup in self.get_group_soups(
                        soup=self.soup, tag=group.tag
                    )
                ],
            )
            for group in self.config.scraping.groups
        ]

    def extract_tags(self):

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

    def extract(self) -> List[ScraperGroupData]:
        # TODO Simplify logic for the extraction
        if self.config.scraping.groups:
            return self.extract_by_group()
        else:
            return self.extract_tags()


def get_group_tags(
    contains: List[str], tags: List[TagScrapingConfig]
) -> List[TagScrapingConfig]:
    # TODO error handling
    return [tag for tag in tags if tag.id in contains]
