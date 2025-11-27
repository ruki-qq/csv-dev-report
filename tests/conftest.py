import csv
import tempfile
from pathlib import Path
from typing import Iterator

import pytest


@pytest.fixture(name="perf_data")
def _sample_data_avg_perf_report() -> list[dict[str, str]]:
    """Valid data for testing AveragePerformanceReport."""

    return [
        {"name": "John", "position": "Backend Developer", "performance": "4.8"},
        {"name": "Jane", "position": "Backend Developer", "performance": "4.6"},
        {"name": "Bob", "position": "Frontend Developer", "performance": "4.7"},
        {"name": "Alice", "position": "Frontend Developer", "performance": "4.9"},
        {"name": "Mike", "position": "QA Engineer", "performance": "4.5"},
    ]


@pytest.fixture(name="invalid_perf_data")
def _invalid_data_avg_perf_report() -> list[dict[str, str]]:
    """Invalid data for testing AveragePerformanceReport."""

    return [{"name": "John", "position": "Developer", "performance": "invalid"}]


@pytest.fixture(name="mixed_perf_data")
def _mixed_valid_invalid_data_avg_perf_report() -> list[dict[str, str]]:
    """Mixed valid and invalid data for testing AveragePerformanceReport."""

    return [
        {"name": "John", "position": "Developer", "performance": "4.5"},
        {"name": "Jane", "position": "Developer", "performance": "invalid"},
        {"name": "Bob", "position": "Developer", "performance": "4.9"},
        {"name": "Alice", "position": "Tester", "performance": ""},
        {"name": "Mike", "position": "Tester", "performance": "4.6"},
    ]


@pytest.fixture(name="float_three_perf_data")
def _float_three_decimal_data_avg_perf_report() -> list[dict[str, str]]:
    """Data with 3 decimal places for testing AveragePerformanceReport."""

    return [
        {"name": "John", "position": "Developer", "performance": "4.333"},
        {"name": "Jane", "position": "Developer", "performance": "4.666"},
    ]


@pytest.fixture
def valid_csv_file(perf_data) -> Iterator[Path]:
    """Creating a temporary CSV file for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=["name", "position", "performance"])
        writer.writeheader()
        writer.writerows(perf_data)
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def invalid_csv_file() -> Iterator[Path]:
    """Creating a temporary invalid CSV file for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("invalid,csv,content\nwith no proper structure")
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def empty_csv_file() -> Iterator[Path]:
    """Creating a temporary empty CSV file for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("empty,csv,file")
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def empty_value_csv_file() -> Iterator[Path]:
    """Creating a temporary CSV file with empty value in row for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,position,performance\n")
        f.write("John,Developer,\n")
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def non_csv_file() -> Iterator[Path]:
    """Creating a temporary non-CSV file for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is not a CSV file")
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def nonexistent_file() -> Path:
    """Path to a non-existent file."""
    return Path("nonexistent_file.csv")


@pytest.fixture
def semicolon_csv_file() -> Iterator[Path]:
    """Creating a temporary semicolon CSV file for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name;position;performance\n")
        f.write("John;Developer;4.6\n")
        f.write("Jane;Designer;4.9\n")
        temp_path = Path(f.name)

    yield temp_path

    temp_path.unlink()


@pytest.fixture
def quotes_csv_file() -> Iterator[Path]:
    """Creating a temporary CSV file with quotes for testing csv_tools."""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,position,performance\n")
        f.write('John,Fake "Developer",4.5\n')
        temp_path = Path(f.name)

    yield temp_path
    temp_path.unlink()


@pytest.fixture
def valid_args() -> list[str]:
    """Valid arguments for testing arg_parser."""

    return ["--files", "file.csv", "--report", "performance"]


@pytest.fixture
def valid_multiple_files_args() -> list[str]:
    """Valid multi-files arguments for testing arg_parser."""

    return ["--files", "file1.csv", "file2.csv", "file3.csv", "--report", "performance"]


@pytest.fixture
def no_files_args() -> list[str]:
    """Invalid arguments without --files for testing arg_parser."""

    return ["--report", "performance"]


@pytest.fixture
def no_report_args() -> list[str]:
    """Invalid arguments without --report for testing arg_parser."""

    return ["--files", "file.csv"]


@pytest.fixture
def abbreviated_args() -> list[str]:
    """Abbreviated arguments for testing arg_parser."""

    return ["--f", "file.csv", "--report", "performance"]


@pytest.fixture
def duplicate_args() -> list[str]:
    """Duplicate arguments for testing arg_parser."""

    return ["--files", "file1.csv", "--files", "file2.csv", "--report", "performance"]


@pytest.fixture
def help_arg() -> list[str]:
    """Help argument for testing arg_parser."""

    return ["--help"]


@pytest.fixture
def unknown_args() -> list[str]:
    """Unknown arguments for testing arg_parser."""

    return ["--files", "file.csv", "--report", "performance", "--unknown", "value"]


@pytest.fixture
def zero_files_args() -> list[str]:
    """Zero-files arguments for testing arg_parser."""

    return ["--files", "--report", "performance"]
