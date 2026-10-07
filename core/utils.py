import os
import re
from pathlib import Path

import yaml


def ensure_parent(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return path


def load_yaml(path, default=None):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or default
    except Exception:
        return default


def save_yaml(path, data):
    ensure_parent(path)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
    return path


def sanitize_filename(value):
    value = (value or '').strip()
    value = re.sub(r'[^A-Za-z0-9_.\- ]+', '_', value)
    value = re.sub(r'\s+', '_', value)
    return value.strip('_') or 'document'
