# Display helpers

def fmt_usd(value):
    return f"${value:,.0f}"

def print_divider(char="-", width=60):
    print(char * width)


def print_stats(label, stats):
    print(f"\n {label}")
    print_divider(".", 40)

    print(f"  Count   : {stats["count"]}")
    print(f"  Mean    : {stats["mean"]}")
    print(f"  Median  : {stats["median"]}")
    print(f"  Max  : {stats["max"]}")
    print(f"  Min  : {stats["min"]}")