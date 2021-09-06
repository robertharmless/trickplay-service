"""
Generic Utilties
"""
# Built-in
from urllib.parse import urlparse

# Special

# App


def get_source_type(source: str) -> str:
    """
    Determine if the source string is a web url or local file path.
    """
    parsed = urlparse(source)
    if parsed.scheme in ["http", "https"]:
        return "url"
    else:
        return "filepath"
