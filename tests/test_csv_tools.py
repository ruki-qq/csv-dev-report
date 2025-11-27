from csv import Error as csv_Error

from pytest import raises as pt_raises

from core import CsvReader


class TestCsvReader:
    """Tests for CsvReader."""

    def test_check_csv_file_valid(self, valid_csv_file):
        """Test validation of a valid CSV file."""

        reader = CsvReader(valid_csv_file)
        result = reader.check_csv_file_valid

        assert "is valid" in result
        assert "5 rows" in result

    def test_check_csv_file_not_found(self, nonexistent_file):
        """Test that non-existent file raises FileNotFoundError."""

        reader = CsvReader(nonexistent_file)

        with pt_raises(FileNotFoundError, match="does not exist"):
            _ = reader.check_csv_file_valid

    def test_check_non_csv_file(self, non_csv_file):
        """Test that non-CSV file raises ValueError."""

        reader = CsvReader(non_csv_file)

        with pt_raises(ValueError, match="is not a CSV file"):
            _ = reader.check_csv_file_valid

    def test_check_empty_csv_file(self, empty_csv_file):
        """Test that empty CSV file raises csv.Error."""

        reader = CsvReader(empty_csv_file)

        with pt_raises(csv_Error, match="is empty"):
            _ = reader.check_csv_file_valid

    def test_check_invalid_csv_structure(self, invalid_csv_file):
        """Test that CSV with inconsistent columns raises csv.Error."""

        reader = CsvReader(invalid_csv_file)

        with pt_raises(csv_Error, match="More or less columns"):
            _ = reader.check_csv_file_valid

    def test_load_csv_returns_list_of_dicts(self, valid_csv_file):
        reader = CsvReader(valid_csv_file)
        data = reader.load_csv

        assert isinstance(data, list)
        assert len(data) == 5
        assert all(isinstance(row, dict) for row in data)

    def test_load_csv_correct_data(self, valid_csv_file):
        reader = CsvReader(valid_csv_file)
        data = reader.load_csv

        assert data[0]["name"] == "John"
        assert data[0]["position"] == "Backend Developer"
        assert data[0]["performance"] == "4.8"
        assert data[1]["name"] == "Jane"
        assert data[1]["position"] == "Backend Developer"
        assert data[1]["performance"] == "4.6"

    def test_load_csv_with_custom_delimiter(self, semicolon_csv_file):
        reader = CsvReader(semicolon_csv_file, delimiter=";")
        data = reader.load_csv

        assert len(data) == 2
        assert data[0]["name"] == "John"
        assert data[0]["position"] == "Developer"

    def test_csv_reader_with_quotes(self, quotes_csv_file):
        """Test CSV reader handles quoted fields."""

        reader = CsvReader(quotes_csv_file)
        data = reader.load_csv

        assert len(data) == 1
        assert data[0]["position"] == 'Fake "Developer"'

    def test_check_csv_file_valid_called_multiple_times(self, valid_csv_file):
        reader = CsvReader(valid_csv_file)

        result1 = reader.check_csv_file_valid
        result2 = reader.check_csv_file_valid

        assert result1 == result2

    def test_load_csv_called_multiple_times(self, valid_csv_file):
        reader = CsvReader(valid_csv_file)

        data1 = reader.load_csv
        data2 = reader.load_csv

        assert data1 == data2
        assert len(data1) == 5
