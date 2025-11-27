import sys
from csv import Error as csv_Error
from pathlib import Path

from core import (
    ArgParser,
    CsvReader,
    ReportRegistry,
    print_table,
    setup_logging,
)
from core.defined_reports import AveragePerformanceReport


def main():
    """Entry point for the application."""

    setup_logging()

    ReportRegistry.register_report("performance", AveragePerformanceReport)

    parser = ArgParser()
    args = parser.parse_args()

    all_data = []
    for file_path in args.files:
        path = Path(file_path)
        reader = CsvReader(path)

        try:
            print(reader.check_csv_file_valid)
        except (FileNotFoundError, ValueError, csv_Error) as e:
            print(f"Error: {e}")
            sys.exit(1)

        data = reader.load_csv
        all_data.extend(data)

    try:
        report_instance = ReportRegistry.get_report(args.report)
        result = report_instance.generate(all_data)

        print_table(
            result, title=f"Report: {args.report.upper()} ({len(all_data)} records)"
        )

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
