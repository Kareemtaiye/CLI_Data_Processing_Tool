import sys
import csv
from display_helper import print_divider, print_stats, fmt_usd
from data_decoder import decode
from stat_helper import compute_statistics, to_float
from data_decoder import EXPERIENCE_MAP, REMOTE_MAP

#Commands
def cmd_summary(rows):
    """Prints a full overview of the dataset"""
    print_divider("=")
    print("  AI/ML DATASET - SUMMARY")
    print_divider("=")
    print(f"\n Total records: {len(rows)}")

    print(f"Columns : {", ".join(rows[0].keys())}")

    #Unique values for key categorical  columns
    for col in ["work_year", "experience_level", "employment_type", "job_titile",  "salary_in_usd"]:
        unique = sorted(set(r.get(col, "") for r in rows))
        print(f"\n Unique {col}s ({len(unique)})")

        for val in unique[:10]: # capture 10 for readability
            decoded = decode({col: val})[col]
            print(f"  {decoded}")


        if len(unique) > 10:
            print(f"  ...and {len(unique) - 10} more.")
            

    # Overall salary stat
    salaries = [to_float(r.get("salary_in_usd") for r in rows)]
    stats = compute_statistics(salaries)
    if stats:
        print()
        print_divider()
        print("  SALARY IN USD - OVERALL STATS")

        print_divider()
        print_stats("Overall roles combined", stats)


    # Stats broken down by experience level
    print()
    print_divider()
    print("  SALARY BY EXPERIENCE LEVEL  ")
    print_divider()
    
    for code, label in EXPERIENCE_MAP.items():
        subset = [to_float(r.get("salary_in_usd")) for r in rows if r.get("experience_level") == code]
        print(subset)
        s = compute_statistics(subset)
        if s:
            print_stats(label, s)

        
    #HTop 5 Highest paying job
    title_salaries = {}


    for row in rows:
        title = row.get("job_title", "Unknown")
        sal = to_float(row.get("salary_in_usd"))

        if sal:
            title_salaries.setdefault(title, []).append(sal) #if there is a title
    avg_by_titile = {t: sum(v) / len(v) for t, v in title_salaries.items()}
    top_titles = sorted(avg_by_titile, key=avg_by_titile.get, reverse=True)[:5]


    print()
    print_divider()
    print("  TOP 5 HIGHEST PAYING JOB (avg USD)")
    print_divider()
    for i, title in enumerate(top_titles, 1):
        print(f"  {i}. {title} {fmt_usd(avg_by_titile[title])}")
        

    # Remote ratio breakdown
    print()
    print_divider()
    print("  REMOTE WORK BREAKDOWN")
    print_divider()

    for code, label in REMOTE_MAP.items():
        count = sum(1 for r in rows if r.get("remote_ratio") == code)
        percentage = (count / len(rows)) * 100
        print(f"  {label}: {count} - ({percentage}%)")

    print()
    print_divider("=")


def cmd_filter(rows, condition):
    """Filter rows by column=value condition"""

    comparison_operators = [">=", "<=","<", "=", ">"]
    found = False

    for op in comparison_operators: # Extended it
        if op in condition:
            found = True
            break
        else:
            continue

    if not found:       
        print(f"[ERROR] --filter format must be a numeric comparison or column=value for non-numeric values. e.g experience_level[{"|".join(comparison_operators)}]SE")
        sys.exit(1)

    print()
    col, val = condition.split(op, 1)
    col = col.strip()
    val = val.strip()

    if rows and col not in rows[0]: #checks if rows(file) is empty or the column doesnt exist on any row(dict)
        print(f"[ERROR] Column '{col}' not found in available colum: ({", ".join(rows[0].keys())})")
        sys.exit(1)
    

    #checking if using numeric operators for non numeric values
    num_operators = [n for n in comparison_operators if n != "="]
    
    if op in num_operators and not to_float(val):
        print(f"[ERROR] Numeric comparison on non-numeric value: {condition}")
        sys.exit(1)

    #Go on to filter
    filtered = []
    if op == ">=":
        filtered = [r for r in rows if to_float(r.get(col)) >= to_float(val)]
    elif op == "<=":
        filtered = [r for r in rows if to_float(r.get(col)) <= to_float(val)]
    elif op == ">":
        filtered = [r for r in rows if to_float(r.get(col)) > to_float(val)]
    elif op == "<":
        filtered = [r for r in rows if to_float(r.get(col)) < to_float(val)]
    else:
        filtered = [r for r in rows if r.get(col, "").lower() == val.lower()] # for "="


    if not filtered:
        print(f"[INFO] No record found for condition '{col}{op}{val}'")
        return []

    print_divider("=")
    print(f"[INFO] FILTER {col} {op} {val}  -->  {len(filtered)} records")

    #Matching rows
    for f in filtered:
        d = decode(f)

        print()
        print(f"  Job             : {d["job_title"]}")
        print(f"  Experience      : {d["experience_level"]}")
        print(f"  Year            : {d["work_year"]}")
        print(f"  Employment Type : {d["employment_type"]}")
        print(f"  Salary          : {fmt_usd(to_float(d["salary_in_usd"]))}")
        print(f"  Location        : {d["company_location"]}")
        print_divider(".", 40)
        print()

    #Extra salary stats
    salaries = [to_float(r.get("salary_in_usd")) for r in filtered]
    salaries_stats = compute_statistics(salaries)
    if salaries_stats:
        print("  SALARY STATS FOR THIS FILTER:")
        print_stats(f"{col} = {val}", salaries_stats)

    return filtered

def cmd_stats(rows, column):
    if rows and column not in rows[0].keys():
        print(f"[ERROR] Column {column} not found in available column {", ".join(rows[0].keys())}")
        sys.exit(1)

    
    values = [to_float(r.get(column)) for r in rows]
    stats = compute_statistics(values)

    if not stats:
        print(f"[ERROR] No numeric data found in column {column}")
        sys.exit(1)

    print_divider("=")
    print(f"  STATS FOR COLUMN: {column}")
    print_divider("=")
    print_stats(column,stats)
    print()

    
def cmd_top(rows, n, column):
    """Show top row sorted by a column"""
    if rows and column not in rows[0]:
        print(f"[ERROR] No column found for {column}. Avail column - {", ".join(rows[0].keys())}")
        sys.exit(1)

    try:
        n = int(n)
    except ValueError:
        print("[ERROR] --top command requires integer. eg --top 5 salary_in_usd")
        sys.exit(1)
    
    def sort_key(r):
        v = to_float(r.get(column))
        return v if not None else -1
    
    sorted_items = sorted(rows, key=sort_key, reverse=True)[:n]

    print_divider("=")
    print(f"\n  TOP {n} RECORDS BY: {column} ")
    print_divider("=")

    for item in sorted_items:
        d = decode(item)

        print()
        print(f"  Job             : {d["job_title"]}")
        print(f"  Experience      : {d["experience_level"]}")
        print(f"  Year            : {d["work_year"]}")
        print(f"  Employment Type : {d["employment_type"]}")
        print(f"  Salary          : {fmt_usd(to_float(d["salary_in_usd"]))}")
        print(f"  Location        : {d["company_location"]}")
        print_divider(".", 40)
        print()

    return sorted_items

def cmd_export(rows, output_path):
    """Export rows to a new csv file"""
    if not rows:
        print("[INFO] No data to export")
        return  
    
    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n [√] Exported {len(rows)} records to: {output_path}")
