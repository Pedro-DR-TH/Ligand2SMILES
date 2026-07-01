import json
import os
from typing import Optional

_DATA_PATH = os.path.join(os.path.dirname(__file__), "ligand_list.json")

def _load():
    with open(_DATA_PATH) as f:
        data = json.load(f)
    return {
        entry["name"].lower(): entry["smiles"]
        for entry in data
        if entry.get("name") and entry.get("smiles") and len(entry.get("smiles", "")) > 3
    }

_LOOKUP = _load()

def name_to_smiles(name: str) -> Optional[str]:
    """
    Look up a compound or ligand name and return its SMILES string.
    Case-insensitive. Returns None if not found.

    Examples
    --------
    >>> name_to_smiles("XPhos")
    'CC(C)C1=CC...'
    >>> name_to_smiles("unknown")
    None
    """
    return _LOOKUP.get(name.strip().lower())


def search(query: str) -> list:
    """
    Search for compounds whose name contains the query string.
    Case-insensitive. Returns a list of {name, smiles} dicts.

    Examples
    --------
    >>> search("phos")
    [{'name': 'XPhos', 'smiles': '...'}, {'name': 'SPhos', 'smiles': '...'}, ...]
    """
    query = query.strip().lower()
    with open(_DATA_PATH) as f:
        data = json.load(f)
    return [
        {"name": entry["name"], "smiles": entry["smiles"]}
        for entry in data
        if entry.get("name") and entry.get("smiles")
        and query in entry["name"].lower()
    ]


def available_names() -> list:
    """
    Return a sorted list of all compound names in the lookup table.

    Examples
    --------
    >>> available_names()
    ['1,10-phenanthroline', 'BINAP', 'BrettPhos', ...]
    """
    with open(_DATA_PATH) as f:
        data = json.load(f)
    return sorted(entry["name"] for entry in data if entry.get("name"))
