import json
from io import TextIOWrapper
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel

from bluescraper.utils import TagDefinition


def load_json(stream: TextIOWrapper) -> dict:
    result = json.load(stream)
    if isinstance(result, dict):
        return result
    raise ValueError


def load_yaml(stream: TextIOWrapper) -> dict:
    result = yaml.safe_load(stream)
    if isinstance(result, dict):
        return result
    raise ValueError


class TagScrapingConfig(BaseModel):
    id: str
    tag: TagDefinition
    content_type: Optional[str] = None


class GroupScrapingConfig(BaseModel):
    id: str
    contains: List[str]
    tag: TagDefinition


class ScrapingConfig(BaseModel):
    tags: List[TagScrapingConfig]
    groups: Optional[List[GroupScrapingConfig]] = None


class ExistingStringInTag(BaseModel):
    include_string: str
    tag: TagDefinition


class ValidationConfig(BaseModel):
    existing_tags: Optional[List[TagDefinition]] = None
    existing_strings_in_tags: Optional[List[ExistingStringInTag]] = None


class Config(BaseModel):
    scraping: ScrapingConfig
    validation: Optional[ValidationConfig] = None


class ConfigReader:
    extension_to_reader_mapping = {
        ".yaml": load_yaml,
        ".yml": load_yaml,
        ".json": load_json,
        ".jsonl": load_json,
    }

    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.file_extension = config_file.suffix
        self.reader = self.extension_to_reader_mapping.get(
            self.file_extension, load_yaml
        )
        self.config_raw: dict = {}

    def read(self) -> dict:
        with open(self.config_file, "r", encoding="utf-8") as stream:
            self.config_raw = self.reader(stream)
        return self.config_raw

    def mapping(self, config_raw: dict) -> Config:
        return Config(**config_raw)

    def load(self) -> Config:
        config_raw = self.read()
        return self.mapping(config_raw)
