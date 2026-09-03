import re

SHOW_HN_PATTERN = re.compile(r"^\s*show\s*hn\s*:\s*", re.IGNORECASE)


def clean_title(title):
    """Strip the 'Show HN:' prefix (case-insensitive) so titles read naturally."""
    return SHOW_HN_PATTERN.sub("", title).strip()