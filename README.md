## AI/ML Salary CLI Tool

A command-line tool for analyzing AI/ML job salary data.

### Features

- Full dataset summary and statistics
- Filter by categorical columns (experience_level, job_title, etc.)
- Filter by numeric comparisons (>, <, >=, <=, =)
- Column statistics
- Top N records by any column
- Export filtered results to CSV

### Usage

python salary_tool.py data.csv --summary
python salary_tool.py data.csv --filter experience_level=SE
python salary_tool.py data.csv --filter salary_in_usd>=100000
python salary_tool.py data.csv --top 5 salary_in_usd
python salary_tool.py data.csv --filter salary_in_usd>=100000 --export results.csv

### Stack

Python — standard library only (csv, argparse, os, sys)
