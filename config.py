"""Configuration loader for the Domino's PL promotions CLI."""

import yaml


def load_config(path: str = "config.yaml") -> dict:
    """Load and return configuration from a YAML file.

    Args:
        path: Path to the YAML config file.

    Returns:
        Parsed configuration dictionary.
    """
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)
