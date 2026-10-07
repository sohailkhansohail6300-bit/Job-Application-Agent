from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def path_from_root(*parts):
    return str(PROJECT_ROOT.joinpath(*parts))
