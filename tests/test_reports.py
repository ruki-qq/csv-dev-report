from pytest import raises as pt_raises

from core import ReportRegistry
from core.defined_reports import AveragePerformanceReport


class TestReportRegistry:
    """Tests for ReportRegistry."""

    def test_register_report(self):
        ReportRegistry.register_report("test_report", AveragePerformanceReport)

        assert "test_report" in ReportRegistry.available_reports

    def test_get_registered_report(self):
        ReportRegistry.register_report("performance", AveragePerformanceReport)
        report = ReportRegistry.get_report("performance")

        assert isinstance(report, AveragePerformanceReport)

    def test_get_nonexistent_report_raises_error(self):
        """Test that getting non-existent report raises ValueError."""

        with pt_raises(ValueError, match="isn't found"):
            ReportRegistry.get_report("nonexistent_report")


class TestAveragePerformanceReport:
    """Tests for AveragePerformanceReport class."""

    def test_generate_report_valid_data(self, perf_data):
        report = AveragePerformanceReport()
        result = report.generate(perf_data)

        assert len(result) == 3
        assert all("position" in item for item in result)
        assert all("performance" in item for item in result)

    def test_generate_report_calculates_average_correct(self, perf_data):
        report = AveragePerformanceReport()
        result = report.generate(perf_data)

        backend_result = next(
            (res for res in result if res["position"] == "Backend Developer"), None
        )
        assert backend_result is not None
        assert backend_result["performance"] == 4.7

        frontend_result = next(
            (res for res in result if res["position"] == "Frontend Developer"), None
        )
        assert frontend_result is not None
        assert frontend_result["performance"] == 4.8

        qa_result = next(
            (res for res in result if res["position"] == "QA Engineer"), None
        )
        assert qa_result is not None
        assert qa_result["performance"] == 4.5

    def test_generate_report_sorting_order(self, perf_data):
        """Test that results are sorted by performance descending."""

        report = AveragePerformanceReport()
        result = report.generate(perf_data)

        assert result[0]["position"] == "Frontend Developer"
        assert result[0]["performance"] == 4.8

        assert result[1]["position"] == "Backend Developer"
        assert result[1]["performance"] == 4.7

        assert result[2]["position"] == "QA Engineer"
        assert result[2]["performance"] == 4.5

    def test_generate_report_empty_data(self):
        report = AveragePerformanceReport()
        result = report.generate([])

        assert result == []

    def test_generate_report_invalid_data(self, invalid_perf_data):
        report = AveragePerformanceReport()
        result = report.generate(invalid_perf_data)

        assert result == []

    def test_generate_report_single_position(self, perf_data):
        data = perf_data[:1]
        report = AveragePerformanceReport()
        result = report.generate(data)

        assert len(result) == 1
        assert result[0]["position"] == "Backend Developer"
        assert result[0]["performance"] == 4.8

    def test_generate_report_mixed_valid_invalid(self, mixed_perf_data):
        """Test report with mixed valid and invalid performance values."""

        report = AveragePerformanceReport()
        result = report.generate(mixed_perf_data)

        assert len(result) == 2

        dev_result = next(
            (res for res in result if res["position"] == "Developer"), None
        )
        assert dev_result is not None
        assert dev_result["performance"] == 4.7

        tester_result = next(
            (res for res in result if res["position"] == "Tester"), None
        )
        assert tester_result is not None
        assert tester_result["performance"] == 4.6

    def test_generate_report_rounding(self, float_three_perf_data):
        """Test that performance values are rounded to 2 decimal places."""

        report = AveragePerformanceReport()
        result = report.generate(float_three_perf_data)

        assert len(result) == 1
        assert result[0]["performance"] == 4.5
