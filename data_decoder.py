# EXPERIENCE LEVEL DECODER(For the particular dataset i am using)
EXPERIENCE_MAP = {
    "EN": "Entry-level",
    "MI": "Mid-level",
    "SE": "Senior",
    "EX": "Executive",
}


EXPLOYMENT_TYPE_MAP = {
    "FT": "Full-Time",
    "PT": "Part-Time",
    "CT": "Contract",
    "FL": "Freelance",
}


REMOTE_MAP = {"0": "Om-site", "50": "Hybrid", "100": "Remote"}


def decode(row):
    """Return human-readable coded file for display"""
    return {
        **row,
        "experience_level": EXPERIENCE_MAP.get(row.get("experience_level", "")),
        "employment_type": EXPLOYMENT_TYPE_MAP.get(row.get("employment_type", "")),
        "remote_ratio": REMOTE_MAP.get(row.get("remote_ratio", "")),
    }
