"""
Built-in verified data source loader.
"""

from pathlib import Path
from typing import Dict, Any
import pandas as pd

from handlers.csv_handler import validate_csv_format, process_uploaded_data


def load_verified_builtin_players() -> Dict[str, Any]:
    """Load verified built-in player dataset from repository CSV."""
    data_path = Path(__file__).resolve().parents[2] / "data" / "verified_players.csv"
    if not data_path.exists():
        return {}

    try:
        df = pd.read_csv(data_path)
        is_valid, _ = validate_csv_format(df)
        if not is_valid:
            return {}
        return process_uploaded_data(df)
    except Exception:
        return {}
