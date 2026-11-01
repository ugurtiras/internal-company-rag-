"""Load and validate the YAML configuration file."""

from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    """Load the YAML config at ``path`` and return it as a plain dict.

    Every tunable value must live in the YAML file; code holds no fallback
    constants, so a missing key surfaces immediately when it is accessed.
    """
    with Path(path).open("r", encoding="utf-8") as file:
        cfg = yaml.safe_load(file)
    if not isinstance(cfg, dict):
        raise ValueError(f"config root must be a mapping, got {type(cfg).__name__}")
    return cfg
