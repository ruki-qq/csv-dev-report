import argparse


class ArgParser(argparse.ArgumentParser):
    """Parsing arguments."""

    def __init__(self):
        super(ArgParser, self).__init__(
            description="Filtering and aggregating CSV files."
        )
        self.add_argument(
            "--files", nargs="+", required=True, help="Path to CSV files."
        )
        self.add_argument(
            "--report",
            required=True,
            help="Creating <report-name> with given files.",
        )
