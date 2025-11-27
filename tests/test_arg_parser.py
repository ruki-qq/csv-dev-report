from pytest import raises as pt_raises

from core import ArgParser


class TestArgParser:
    """Tests for ArgParser class."""

    def test_parse_single_file(self, valid_args):
        parser = ArgParser()
        args = parser.parse_args(valid_args)

        assert args.files == ["file.csv"]
        assert args.report == "performance"

    def test_parse_multiple_files(self, valid_multiple_files_args):
        parser = ArgParser()
        args = parser.parse_args(valid_multiple_files_args)

        assert len(args.files) == 3
        assert args.files == ["file1.csv", "file2.csv", "file3.csv"]
        assert args.report == "performance"

    def test_missing_files_argument_raises_error(self, no_files_args):
        """Test that missing --files raises SystemExit."""

        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(no_files_args)

    def test_missing_report_argument_raises_error(self, no_report_args):
        """Test that missing --report raises SystemExit."""

        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(no_report_args)

    def test_missing_all_arguments_raises_error(self):
        """Test that missing all arguments raises SystemExit."""

        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args([])

    def test_abbreviation_not_allowed(self, abbreviated_args):
        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(abbreviated_args)

    def test_duplicate_argument_raises_error(self, duplicate_args):
        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(duplicate_args)

    def test_help_argument(self, help_arg):
        parser = ArgParser()
        with pt_raises(SystemExit) as exc_info:
            parser.parse_args(help_arg)

        assert exc_info.value.code == 0

    def test_unknown_argument_raises_error(self, unknown_args):
        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(unknown_args)

    def test_files_without_values_raises_error(self, zero_files_args):
        parser = ArgParser()
        with pt_raises(SystemExit):
            parser.parse_args(zero_files_args)
