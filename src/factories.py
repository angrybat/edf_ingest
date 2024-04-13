from json import load
from pathlib import Path

from src.models import Settings


def get_settings(file_path: Path) -> Settings:
    with open(file_path) as file:
        json = load(file)
        return Settings(**json)
