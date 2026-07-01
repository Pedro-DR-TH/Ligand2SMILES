import json
import os
from typing import Optional

#load JSON once at start
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

    Parameters
    ----------
    name : str
        Common name, trade name, or IUPAC name of the compound.

    Returns
    -------
    str or None
        SMILES string if found, None otherwise.

    Examples
    --------
    >>> name_to_smiles("XPhos")
    'CC(C)C1=CC(=C(C(=C1)C(C)C)...'
    >>> name_to_smiles("triphenylphosphine")
    'C1=CC=C(C=C1)P(C2=CC=CC=C2)...'
    >>> name_to_smiles("unknown_ligand")
    None
    """
    return _LOOKUP.get(name.strip().lower())


def search(query: str) -> list[dict]:
    """
    Search for compounds whose name contains the query string.
    Case-insensitive. Returns a list of {name, smiles} dicts.

    Parameters
    ----------
    query : str
        Partial or full name to search for.

    Returns
    -------
    list of dict
        Each dict has keys 'name' and 'smiles'.

    Examples
    --------
    >>> search("xphos")
    [{'name': 'XPhos', 'smiles': '...'}]
    >>> search("phos")
    [{'name': 'XPhos', ...}, {'name': 'SPhos', ...}, ...]
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


def available_names() -> list[str]:
    """
    Return a sorted list of all compound names in the lookup table.

    Returns
    -------
    list of str
    """
    with open(_DATA_PATH) as f:
        data = json.load(f)
    return sorted(entry["name"] for entry in data if entry.get("name"))
