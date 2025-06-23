from pathlib import Path
from functools import lru_cache
from typing import Dict, List

import pandas as pd 



@lru_cache(maxsize=1)
def _load_airports() -> pd.DataFrame:
    csv_path = Path(__file__).with_name("airports.csv")
    return pd.read_csv(csv_path, dtype=str)

def get_iata_code(city: str) -> Dict[str, object]:
    """
    Look up IATA airport codes that serve a given city.

    Args:
        city (str): Name of the city (e.g., "New York").

    Returns:
        dict:
          • On success → {"status": "success",
                          "city": "<City>",
                          "iata_codes": ["JFK", "LGA", ...]}
          • On failure → {"status": "error",
                          "city": "<City>",
                          "message": "No IATA codes found for <City>"}
    """
    df = _load_airports()

    mask   = df["City"].str.strip().str.lower() == city.strip().lower()
    codes: List[str] = (
        df.loc[mask, "IATA"]
          .dropna()
          .unique()
          .tolist()
    )

    if codes:
        return {"status": "success", "city": city.title(), "iata_codes": codes}

    return {"status": "error", "city": city.title(),
            "message": f"No IATA codes found for {city!r}"}



def get_airport_name(iata_code: str) -> Dict[str, object]:
    """
    Look up the official airport name(s) for a given IATA code.

    Args:
        iata_code (str): Three-letter airport code, e.g. "JFK".

    Returns:
        dict
          • Success → {"status": "success",
                       "iata": "JFK",
                       "airport_names": ["John F. Kennedy International Airport"],
                       "city": "New York"}
          • Failure → {"status": "error",
                       "iata": "ZZZ",
                       "message": "No airport found for IATA 'ZZZ'"}
    """
    df   = _load_airports()                 
    code = iata_code.strip().upper()

    mask = df["IATA"].str.upper() == code
    if not mask.any():
        return {"status": "error",
                "iata": code,
                "message": f"No airport found for IATA '{code}'"}

    rows = df[mask]

    name_col = "Airport name"
    airport_names: List[str] = rows[name_col].dropna().unique().tolist()

    result: Dict[str, object] = {"status": "success",
                                 "iata": code,
                                 "airport_names": airport_names,
                                 "city":rows.iloc[0]["City"]
                                 }

    return result
