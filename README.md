# Ligand2SMILES

A lightweight Python module for looking up SMILES strings from compound and ligand names.
Built from Wikidata (P2017/P233) and PubChem, with a curated list of phosphine ligands
including the full Buchwald monophosphine family, bisphosphines, NHC ligands, and more.

## Installation

```bash
git clone https://github.com/Pedro-DR-TH/Ligand2SMILES
cd Ligand2SMILES
pip install .
```

No dependencies beyond the Python standard library. The lookup database is included, no setup or any scraping is required.

All entries are validated through RDKit and cross-checked against source molecular weights (entries with a discrepancy of ≥1 Da were removed) before inclusion in the database.


## Usage

### Exact name lookup

```python
from Ligand2SMILES import name_to_smiles

smiles = name_to_smiles("XPhos")
# 'CC(C)C1=CC(=C(C(=C1)C(C)C)...'

smiles = name_to_smiles("triphenylphosphine")
# 'C1=CC=C(C=C1)P(C2=CC=CC=C2)C3=CC=CC=C3'

smiles = name_to_smiles("unknown")
# None
```

### Partial name search

```python
from Ligand2SMILES import search

results = search("phos")
# [{'name': 'XPhos', 'smiles': '...'}, {'name': 'SPhos', 'smiles': '...'}, ...]
```

### List all available names

```python
from Ligand2SMILES import available_names

names = available_names()
# ['1,10-phenanthroline', 'BINAP', 'BrettPhos', 'XPhos', ...]
```

## Coverage

~12000+ compounds including:
- Buchwald monophosphines (XPhos, SPhos, RuPhos, BrettPhos, DavePhos, JohnPhos, ...)
- Bisphosphines (BINAP, DPPF, dppe, Xantphos, SEGPHOS, ...)
- NHC ligands (IMes, IPr, SIMes, SIPr, ...)
- SelectPhos family (SelectPhos, CySelectPhos, PhSelectPhos)
- Nitrogen donors (1,10-phenanthroline, 2,2-bipyridine, ...)
- General compounds from Wikidata

## Data sources

- **Wikidata**: SPARQL queries for P2017 (isomeric SMILES) and P233 (canonical SMILES)
- **PubChem**: CAS number and systematic name lookups for specialty phosphine ligands not in Wikidata

Found something wrong?
Let me know here: https://forms.gle/jbzANwcuArx13yis5

Thank you!
