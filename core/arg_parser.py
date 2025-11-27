import argparse


class OnceAction(argparse.Action):
    """Action that allows argument to be specified only once."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.error(f"Argument {option_string}: not allowed more than once")
        setattr(namespace, self.dest, values)


class ArgParser(argparse.ArgumentParser):
    """Parsing arguments."""

    def __init__(self):
        super(ArgParser, self).__init__(
            description="Filtering and aggregating CSV files.",
            allow_abbrev=False,
        )
        self.add_argument(
            "--files",
            nargs="+",
            required=True,
            action=OnceAction,
            help="Path to CSV files.",
        )
        self.add_argument(
            "--report",
            required=True,
            action=OnceAction,
            help="Creating <report-name> with given files.",
        )
