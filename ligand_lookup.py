import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "wikidata_smiles.json")

with open(_DATA_PATH) as f:
    _data = json.load(f)

_LOOKUP = {entry["name"].lower(): entry["smiles"] for entry in _data if entry.get("name") and entry.get("smiles")}

def name_to_smiles(name: str) -> str | None:
    """
    Look up a compound or ligand name and return its SMILES string.
    Returns None if not found.
    
    Example:
        >>> name_to_smiles("XPhos")
        'CC(C)C1=CC...'
        >>> name_to_smiles("triphenylphosphine")
        'C1=CC=C(C=C1)P...'
    """
    return _LOOKUP.get(name.lower())
