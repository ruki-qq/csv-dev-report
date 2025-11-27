from abc import ABC, abstractmethod
from typing import Any

from .logger import log


class BaseReport(ABC):
    """Base report class."""

    @abstractmethod
    def generate(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Generate report from data.

        Args:
            data: list of dictionaries with some data.

        Returns:
            List of dictionaries for further operations.
        """

        raise NotImplementedError


class ReportRegMeta(type):
    """Metaclass for report registry."""

    @property
    def available_reports(cls) -> list[str]:
        """
        Getting available reports.

        Returns:
            List of available report names.
        """
        return list(cls._reports)  # type: ignore[attr-defined]


class ReportRegistry(metaclass=ReportRegMeta):
    """Registry of available reports."""

    _reports: dict["str", type[BaseReport]] = {}

    @classmethod
    @log
    def get_report(cls, report_name: str) -> BaseReport:
        """
        Getting report instance.

        Args:
            report_name: report name.

        Returns:
            Report class instance.

        Raises:
            ValueError: If report name is not found.
        """

        if report_name not in cls._reports:
            error_msg = (
                f"Report '{report_name}' isn't found. "
                f"Available reports: {', '.join(cls._reports)}".rstrip()
            )
            raise ValueError(error_msg)

        return cls._reports[report_name]()

    @classmethod
    @log
    def register_report(
        cls, report_name: str, report_class: type[BaseReport]
    ) -> type[BaseReport]:
        """
        Registering report class.

        Args:
            report_name: report name.
            report_class: report class.

        Returns:
            Registered report class.
        """

        cls._reports[report_name] = report_class
        return report_class
