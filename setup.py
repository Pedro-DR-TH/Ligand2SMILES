from setuptools import setup, find_packages

setup(
    name="Ligand2SMILES",
    version="0.1.0",
    packages=find_packages(),
    package_data={"Ligand2SMILES": ["ligand_list.json"]},
    python_requires=">=3.9",
)
