import datetime
import os

import pytest
from bs4 import BeautifulSoup

import bluescraper.config
from bluescraper import constants, fileutils, utils, validation


def test_create_file_path_from_date(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = fileutils.DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    assert (
        true_file_path == dateDirectoryTreeCreator.create_file_path_from_date()
    )


def test_make_dir_tree_from_date(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = fileutils.DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    dateDirectoryTreeCreator.make_dir_tree_from_date()
    assert true_file_path


def test_make_dir_tree_from_file_path(tmp_path) -> None:
    true_file_path = os.path.join(tmp_path, "2022/01")
    dateDirectoryTreeCreator = fileutils.DateDirectoryTreeCreator(
        date_=datetime.date(2022, 1, 12),
        date_pattern="%Y/%m",
        root_dir=tmp_path,
    )
    dateDirectoryTreeCreator.make_dir_tree_from_file_path(true_file_path)
    assert true_file_path


def test_create_file_name_from_date() -> None:
    date_ = datetime.date(2022, 1, 12)
    true_file_name = "prefix_2022-01-12_suffix.json"
    assert true_file_name == fileutils.create_file_name_from_date(
        date_, prefix="prefix_", suffix="_suffix", extension=".json"
    )


def test_create_file_name_from_datetime() -> None:
    datetime_ = datetime.datetime(2022, 1, 12, 11, 12, 30)
    true_file_name = "prefix_2022-01-12T11:12:30_suffix.json"
    assert true_file_name == fileutils.create_file_name_from_date(
        datetime_, prefix="prefix_", suffix="_suffix", extension=".json"
    )


def test_normalize_datetime() -> None:
    assert (
        utils.transform_datetime_str("30.01.2021 - 18:04 Uhr")
        == "2021-01-30 18:04:00"
    )


def test_get_date_range() -> None:
    expected_result = [
        datetime.date(2022, 1, 1),
        datetime.date(2022, 1, 2),
        datetime.date(2022, 1, 3),
        datetime.date(2022, 1, 4),
    ]
    assert (
        utils.get_date_range(
            datetime.date(2022, 1, 1), datetime.date(2022, 1, 5)
        )
        == expected_result
    )


def test_clean_string():
    input_string = " test      \nthis\n  thing        "
    expected_clean_string = "test this thing"
    cleaned_string = utils.clean_string(input_string)
    assert cleaned_string == expected_clean_string


@pytest.mark.parametrize(
    argnames="html, key, tag_definition, expected",
    argvalues=[
        pytest.param(
            constants.VALID_HTML_PATH,
            "href",
            utils.TagDefinition(
                name="a", attrs={"class": "teaser-right__link"}
            ),
            "/dummy/article.html",
            id="href",
        ),
        pytest.param(
            constants.VALID_HTML_PATH,
            "data-teaserdate",
            utils.TagDefinition(
                name="div", attrs={"class": "teaser-right twelve"}
            ),
            "1696763839",
            id="teaserdate",
        ),
        pytest.param(
            constants.VALID_HTML_PATH,
            None,
            utils.TagDefinition(
                name="span", attrs={"class": "teaser-right__labeltopline"}
            ),
            "Test topline",
            id="text",
        ),
    ],
    indirect=["html"],
)
def test_extract_from_tag_by_key(soup, key, tag_definition, expected):
    tag = soup.find(name=tag_definition.name, attrs=tag_definition.attrs)
    text = utils.extract_from_tag(tag, attribute=key)
    assert text == expected


def test_extract_text_from_tag():
    expected_text = "This is /n some sample text!"
    html_with_text = f'<span class="text">{expected_text}</span>'
    tag_with_text = BeautifulSoup(html_with_text, "html.parser").span
    text = utils.extract_text(tag_with_text)  # type: ignore
    assert text == expected_text


@pytest.mark.parametrize(
    argnames="html", argvalues=[constants.VALID_HTML_PATH], indirect=True
)
def test_is_text_in_tag(soup):
    tag_definition = utils.TagDefinition(
        name="span", attrs={"class": "teaser-right__labeltopline"}
    )
    example_text = " topline"
    assert utils.is_text_in_tag(soup, tag_definition, example_text)


@pytest.mark.parametrize(
    argnames="html", argvalues=[constants.VALID_HTML_PATH], indirect=True
)
def test_is_tag_in_soup(soup):
    tag_definition = utils.TagDefinition(
        name="span", attrs={"class": "teaser-right__headline"}
    )
    assert utils.is_tag_in_soup(soup, tag_definition)


@pytest.mark.parametrize(
    argnames="html", argvalues=[constants.VALID_HTML_PATH], indirect=True
)
def test_validator_with_validation_content(soup):
    existing_tags = [
        utils.TagDefinition(name=name, attrs=attrs)
        for name, attrs in [
            ("span", {"class": "teaser-right__labeltopline"}),
            ("span", {"class": "teaser-right__headline"}),
            (None, {"class": "teaser-right__shorttext"}),
        ]
    ]
    existing_strings_in_tags = [
        bluescraper.config.ExistingStringInTag(
            include_string=include_string,
            tag=utils.TagDefinition(name=name, attrs=attrs),
        )
        for include_string, name, attrs in [
            ("Test topline", "span", {"class": "teaser-right__labeltopline"}),
            ("headline", "span", {"class": "teaser-right__headline"}),
        ]
    ]

    validation_config = bluescraper.config.ValidationConfig(
        existing_tags=existing_tags,
        existing_strings_in_tags=existing_strings_in_tags,
    )
    validator = validation.SoapValidator(soup, validation_config)
    validator.validate()
    assert validator.valid
