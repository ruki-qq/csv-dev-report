# csv-dev-report

This project is for generating reports from CSV files.
It's currently supports performance report, though new reports can be added by creating BaseReport child class and register it in ReportRegistry with ReportRegistry.register_report.

## Usage

```bash
poetry install
python main.py --files <paths_to_csv_files> --report <report_name>
```

## Examples

```bash
python main.py --files csv/employees1.csv csv/employees2.csv --report performance
```

## Testing

```bash
python -m pytest
```

## Screenshots

### Basic usage
![alt](https://files.catbox.moe/80kn2b.png)

![alt](https://files.catbox.moe/7sjesj.png)


### Some error handling
![alt](https://files.catbox.moe/uj2i3s.png)


### Tests & flake8
![alt](https://files.catbox.moe/p10jgw.png)


### Logs
![alt](https://files.catbox.moe/t9xemk.png)
