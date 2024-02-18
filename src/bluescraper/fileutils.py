import datetime
import os
from typing import Optional, Union


class DateDirectoryTreeCreator:
    """
    Create a directory tree and file name based on a date object.
    """

    def __init__(
        self,
        date_: datetime.date,
        date_pattern: str = "%Y/%m",
        root_dir: str = ".",
    ) -> None:
        """
        Initialize parameters and make the directory tree.

        Parameters
        ----------
        date_ : date, Provided date object
        date_pattern : str, optional
            The date pattern describes the directory structure, by default
            "%Y/%m"
        root_dir : str, optional
            The base directory where the directory tree will be generated, by
            default current directory ('.').
        """
        self.date_pattern = date_pattern
        self.date_ = date_
        self.root_dir = root_dir

    def create_file_path_from_date(
        self,
    ):
        """
        Create a hierarchical file path from the given date object without
        creating directories.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure.
            Default date pattern from class initialization will be used when no
            pattern is provided.
        root_dir : str, optional
            The base directory where the directory tree will be generated.
            Default root directory from class initialization will be used when
            no directory is provided.
        """
        file_path = os.path.join(
            self.root_dir, self.date_.strftime(self.date_pattern)
        )
        return file_path

    def make_dir_tree_from_date(
        self,
    ) -> None:
        """
        Make a hierarchical directory tree from the given date object.

        Parameters
        ----------
        date_pattern : str, optional
            The date pattern describes the directory structure.
            Default date pattern from class initialization will be used when
            no pattern is provided.
        root_dir : str, optional
            The base directory where the directory tree will be generated.
            Default root directory from class initialization will be used when
            no directory is provided.
        """
        file_path = self.create_file_path_from_date()
        self.make_dir_tree_from_file_path(file_path)

    def make_dir_tree_from_file_path(self, file_path: str) -> None:
        os.makedirs(file_path, exist_ok=True)


def create_file_name_from_date(
    date_or_datetime: Union[datetime.date, datetime.datetime],
    date_pattern: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    extension: str = "",
) -> str:
    """
    Create a file name from a date object.

    Parameters
    ----------
    date_ : Union[date, datetime]
        Provided date or datetime object.
    date_pattern : str, optional
        Date pattern in file name, by default "%Y-%m-%d"
    prefix : str, optional
        String before date pattern, by default ""
    suffix : str, optional
        String after date pattern, by default ""
    extension : str, optional
        File extension including ., e.g. '.csv' or '.json', by default ""

    Returns
    -------
    str
    The full file name.
    """
    if date_pattern is None:
        if isinstance(date_or_datetime, datetime.datetime):
            formatted_date = date_or_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            formatted_date = date_or_datetime.strftime("%Y-%m-%d")
    else:
        formatted_date = date_or_datetime.strftime(date_pattern)
    file_name = prefix + formatted_date + suffix + extension
    return file_name
