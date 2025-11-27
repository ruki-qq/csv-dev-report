import csv
from pathlib import Path

from .logger import log


class CsvReader:
    def __init__(self, file: Path, delimiter: str = ","):
        self.file = file
        self.delimiter = delimiter

    @property
    @log
    def check_csv_file_valid(self) -> str:
        """
        Checking if csv file exists.

        Returns:
            Valid log info-string.

        Raises:
            FileNotFoundError: If csv file does not exist.
            ValueError: If file is not a csv file.
            csv.Error: If file validation fails.
        """

        if not self.file.is_file():
            error_msg = f"File {self.file} does not exist!"
            raise FileNotFoundError(error_msg)

        if not self.file.suffix == ".csv":
            error_msg = f"File {self.file} is not a CSV file!"
            raise ValueError(error_msg)

        with open(self.file, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            header = next(reader)
            header_count = len(header)
            rows = list(reader)

            if len(rows) == 0:
                error_msg = f"CSV file {self.file} is empty!"
                raise csv.Error(error_msg)

            for row in rows:
                if len(row) != header_count:
                    error_msg = f"More or less columns than headers in row: {row}"
                    raise csv.Error(error_msg)
                for value in row:
                    if not value:
                        error_msg = f"Empty value in row: {row}"
                        raise csv.Error(error_msg)

            return f"CSV file {self.file} is valid with {len(rows)} rows."

    @property
    @log
    def load_csv(self) -> list[dict[str, str]]:
        """
        Loading CSV file.

        Returns: List of dictionaries from CSV file.
        """

        with open(self.file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            data = list(reader)

        return data
