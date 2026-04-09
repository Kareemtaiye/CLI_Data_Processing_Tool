from html import parser
from loader import load_csv
from cmd_helper import (
    cmd_export,
    cmd_filter,
    cmd_stats,
    cmd_summary,
    cmd_top,
)
from arg_parser import build_parser

"""
AI/ML Salary Data CLI Tool
Usage examples:
    python salary_tool.py data.csv --summary
    python salary_tool.py data.csv --filter experience_level=SE - EXTENDED: Now supports numeric comparison e.g salary_in_usd
    python salary_tool.py data.csv --stats salary_in_usd
    python salary_tool.py data.csv --top 5 salary_in_usd
    python salary_tool.py data.csv --filter job_title=ML Engineer --export results.csv
"""


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
