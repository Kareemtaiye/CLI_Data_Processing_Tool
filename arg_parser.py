import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="AI/ML Salary Dataset CLI Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python salary_tool.py data.csv --summary
  python salary_tool.py data.csv --filter experience_level=SE
  python salary_tool.py data.csv --filter job_title=ML Engineer
  python salary_tool.py data.csv --stats salary_in_usd
  python salary_tool.py data.csv --top 5 salary_in_usd
  python salary_tool.py data.csv --filter experience_level=SE --export senior.csv
        """,
    )

    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument(
        "--summary", action="store_true", help="Show full dataset summary"
    )
    parser.add_argument(
        "--filter",
        metavar=["col=value", "col>value", "col<=value"],
        help="Filter rows by numneric comparisons",
    )
    parser.add_argument(
        "--stats", metavar="column", help="Show stats for a numeric column"
    )
    parser.add_argument(
        "--top", nargs=2, metavar=("N", "column"), help="Show top N rows by column"
    )
    parser.add_argument("--export", metavar="output.csv", help="Export results to CSV")
    return parser
