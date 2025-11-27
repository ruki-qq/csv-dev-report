from collections import defaultdict
from typing import Any

from core import BaseReport, convert_to_number, is_numeric, log


class AveragePerformanceReport(BaseReport):
    """Report for average performances by dev's position."""

    @log
    def generate(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Generating report with developers performance by position.

        Args:
            data: List of dictionaries with products data.

        Returns:
            List of dictionaries with brands and their avf ratings,
            sorted by rating(desc).
        """

        position_perf = defaultdict(list)

        for developer in data:
            position = developer["position"]
            performance = developer["performance"]

            if not is_numeric(performance):
                continue

            performance = convert_to_number(performance)
            position_perf[position].append(performance)

        report_data = []
        for position, performances in position_perf.items():
            avg_performance = sum(performances) / len(performances)
            report_data.append(
                {"position": position, "performance": round(avg_performance, 2)}
            )

        report_data.sort(key=lambda x: x["performance"], reverse=True)

        return report_data
