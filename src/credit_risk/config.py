"""Load project configuration from configs/*.toml."""

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "configs"


def load_config(name: str = "uci_taiwan") -> dict:
    """Return the named config, with entries under [paths] resolved against the project root."""
    with open(CONFIG_DIR / f"{name}.toml", "rb") as f:
        config = tomllib.load(f)
    for key, value in config.get("paths", {}).items():
        config["paths"][key] = PROJECT_ROOT / value
    return config
