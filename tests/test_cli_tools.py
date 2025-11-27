from core import print_table


class TestPrintTable:
    """Tests for print_table function."""

    def test_print_table_with_valid_data(self, capsys, perf_data):
        print_table(perf_data)
        captured = capsys.readouterr()

        assert "John" in captured.out
        assert "Jane" in captured.out
        assert "name" in captured.out
        assert "position" in captured.out
        assert "performance" in captured.out
        assert "4.8" in captured.out

    def test_print_table_with_title(self, capsys, perf_data):
        title = "Test Results"
        print_table(perf_data, title=title)
        captured = capsys.readouterr()

        assert title in captured.out
        assert "=" * len(title) in captured.out
        assert "John" in captured.out

    def test_print_table_empty_data(self, capsys):
        print_table([])
        captured = capsys.readouterr()

        assert "No data to display" in captured.out

    def test_print_table_single_row(self, capsys, perf_data):
        data = perf_data[:1]
        print_table(data)
        captured = capsys.readouterr()

        assert "Backend Developer" in captured.out
        assert "4.8" in captured.out

    def test_print_table_grid_format(self, capsys, perf_data):
        """Test that table uses grid format."""

        print_table(perf_data)
        captured = capsys.readouterr()

        assert "+" in captured.out
        assert "|" in captured.out
