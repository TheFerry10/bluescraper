from pathlib import Path

DEFAULT_TIMEOUT = None
TEST_HTML_DIR = Path("tests/data/bluescraper/html/")
TEST_CONFIG_DIR = Path("tests/data/bluescraper/config/")
VALID_HTML_PATH = TEST_HTML_DIR.joinpath("valid.html")
VALID_GROUPS_HTML_PATH = TEST_HTML_DIR.joinpath("valid-groups.html")
VALID_GROUPS_GROUP_NOT_COMPLETE_HTML_PATH = TEST_HTML_DIR.joinpath(
    "valid-groups-group-not-complete.html"
)
INVALID_HTML_PATH = TEST_HTML_DIR.joinpath("invalid.html")
CONFIG_YAML = TEST_CONFIG_DIR.joinpath("config.yml")
INVALID_CONFIG_YAML = TEST_CONFIG_DIR.joinpath("invalid-config.yml")
CONFIG_GROUPS_YAML = TEST_CONFIG_DIR.joinpath("config-groups.yml")
CONFIG_MULTIPLE_GROUPS_YAML = TEST_CONFIG_DIR.joinpath(
    "config-multiple-groups.yml"
)
CONFIG_NO_VALIDATION_YAML = TEST_CONFIG_DIR.joinpath(
    "config-no-validation.yml"
)
CONFIG_JSON = TEST_CONFIG_DIR.joinpath("config.json")
GROUPS_HANDELSBLATT_HTML_PATH = TEST_HTML_DIR.joinpath("handelsblatt.html")
CONFIG_HANDELSBLATT_GROUPS_HTML_YAML = TEST_CONFIG_DIR.joinpath(
    "config-handelsblatt.yml"
)
