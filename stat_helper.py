# Statistic helpers
def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def compute_statistics(values):
    """Return dict of basic stats for numeric list"""
    clean_data = [v for v in values if v is not None]
    if not clean_data:
        return None

    clean_data.sort()
    n = len(clean_data)
    mean = sum(clean_data) // n
    mid = n // 2

    if n == 1:
        median = clean_data[0]  # only one element
    elif n == 2:
        median = clean_data[0] + clean_data[1] // 2
    else:
        median = (
            clean_data[mid]
            if n % 2 != 0  # if one median, 1
            else clean_data[mid - 1] + clean_data[mid + 1] // 2  # if two median
        )

    return {
        "count": n,
        "mean": mean,
        "median": median,
        "min": clean_data[0],
        "max": clean_data[-1],
    }
