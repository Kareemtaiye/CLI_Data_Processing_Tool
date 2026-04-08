"""
AI/ML Salary Data CLI Tool
Usage examples:
    python salary_tool.py data.csv --summary
    python salary_tool.py data.csv --filter experience_level=SE
    python salary_tool.py data.csv --stats salary_in_usd
    python salary_tool.py data.csv --top 5 salary_in_usd
    python salary_tool.py data.csv --filter job_title=ML Engineer --export results.csv
"""

import argparse
from html import parser
from loader import load_csv
from cmd_helper import (
    cmd_export,
    cmd_filter,
    cmd_stats,
    cmd_summary,
    cmd_top,
    compute_statistics,
)


# Argument Parser
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
        "--filter", metavar="col=value", help="Filter rows by column=value"
    )
    parser.add_argument(
        "--stats", metavar="column", help="Show stats for a numeric column"
    )
    parser.add_argument(
        "--top", nargs=2, metavar=("N", "column"), help="Show top N rows by column"
    )
    parser.add_argument("--export", metavar="output.csv", help="Export results to CSV")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    rows = load_csv(args.file)
    result_rows = rows  # may be narrowed by --filter

    if args.filter:
        result_rows = cmd_filter(rows, args.filter)

    if args.summary:
        cmd_summary(rows)

    if args.stats:
        cmd_stats(result_rows, args.stats)

    if args.top:
        n, column = args.top
        cmd_top(result_rows, n, column)

    if args.export:
        cmd_export(result_rows, args.export)

    # Default: if no command given beyond the file, show summary
    if not any([args.summary, args.filter, args.stats, args.top, args.export]):
        cmd_summary(rows)


if __name__ == "__main__":
    main()

# data = load_csv(sys.argv[1])
# info = compute_statistics([to_float(d["salary_in_usd"]) for d in data])
# # print_stats("salaries", info)
# # cmd_summary(data)
# # cmd_filter(data, sys.argv[2])
# # cmd_stats(data, sys.argv[2])
# print(sys.argv)
# cmd_export(cmd_top(data, sys.argv[2], sys.argv[3]), sys.argv[4])
