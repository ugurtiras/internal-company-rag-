"""Split a markdown file into (metadata dict, body text)."""

import yaml


def split_front_matter(content: str) -> tuple[dict, str]:
    """Return the front matter as a dict and the remaining text.

    Raises ValueError if the file has no valid front matter.
    """
    content = content.lstrip("\ufeff")
    if not content.startswith("---"):
        raise ValueError("no front matter found")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("front matter is not closed")

    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError("front matter is not a mapping")

    return metadata, parts[2].strip()
