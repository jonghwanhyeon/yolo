import os
import re


def is_production() -> bool:
    value = os.environ.get("YOLO_ENV", "production")
    return value.lower() == "production"


def is_development() -> bool:
    value = os.environ.get("YOLO_ENV", "production")
    return value.lower() == "development"


def only_digits(text):
    return re.sub(r"[^0-9]", "", text)
