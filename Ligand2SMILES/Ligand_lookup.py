import json
import os
from typing import Optional
from difflib import SequenceMatcher

_DATA_PATH = os.path.join(os.path.dirname(__file__), "ligand_list.json")

def _load():
    with open(_DATA_PATH) as f:
        data = json.load(f)
    if isinstance(data, dict):
        return {k.lower(): v for k, v in data.items()}
    return {entry["name"].lower(): entry["smiles"] for entry in data if entry.get("name") and entry.get("smiles")}

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
    [{'name': 'XPhos', 'smiles': '...'}, ...]
    """
    query = query.strip().lower()
    with open(_DATA_PATH) as f:
        data = json.load(f)
    if isinstance(data, dict):
        return [{"name": k, "smiles": v} for k, v in data.items() if query in k.lower()]
    return [
        {"name": e["name"], "smiles": e["smiles"]}
        for e in data
        if e.get("name") and e.get("smiles") and query in e["name"].lower()
    ]


def fuzzy_search(name: str, threshold: float = 0.6, top_n: int = 5) -> list:
    """
    Search for compounds using fuzzy string matching.
    Useful for handling typos, OCR errors, and abbreviation variants.
    Returns top matches above the similarity threshold.

    Parameters
    ----------
    name : str
        The name to search for (can be misspelled or abbreviated).
    threshold : float
        Minimum similarity score (0-1). Default 0.6.
    top_n : int
        Maximum number of results to return. Default 5.

    Returns
    -------
    list of dict
        Each dict has keys 'name', 'smiles', 'score'.
        Sorted by score descending.

    Examples
    --------
    >>> fuzzy_search("xphos")
    [{'name': 'XPhos', 'smiles': '...', 'score': 1.0}]
    >>> fuzzy_search("triphenylphospine")  # typo
    [{'name': 'triphenylphosphine', 'smiles': '...', 'score': 0.97}]
    """
    query = name.strip().lower()
    results = []

    for key, smiles in _LOOKUP.items():
        score = SequenceMatcher(None, query, key).ratio()
        if score >= threshold:
            results.append({"name": key, "smiles": smiles, "score": round(score, 3)})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


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
    if isinstance(data, dict):
        return sorted(data.keys())
    return sorted(e["name"] for e in data if e.get("name"))
