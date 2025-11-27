from tabulate import tabulate

from .logger import log


@log
def print_table(data: list[dict], title: str = "") -> None:
    """
    Printing data as a table to console.

    Args:
        data: List of dictionaries to display.
        title: Optional title for the table.
    """

    if not data:
        print("No data to display.")
        return

    if title:
        print(f"\n{title}")
        print("=" * len(title))

    print(
        tabulate(
            data,
            headers="keys",
            tablefmt="grid",
            numalign="right",
            stralign="left",
        )
    )
    print()
