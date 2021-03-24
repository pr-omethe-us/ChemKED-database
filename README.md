# ChemKED-database

[![DOI](https://zenodo.org/badge/84258934.svg)](https://zenodo.org/badge/latestdoi/84258934)
[![Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg)](http://contributor-covenant.org/version/1/4/)

Database of ChemKED files for fundamental combustion experiments

License
-------
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
See the LICENSE.txt file or follow the link for details.

Submissions: Sine qua none
--------------------------
1. All yaml files require a permanent link, prefereably a DOI, although arXiv identifiers should also be sufficient. These identifiers must be present in each and every file.
2. Each file requires at least one identified person in the `"file-authors"` field, preferable with ORCID to establish a corresponding author for the dataset. This is to ensure that missing or malformed information may be corrected in the future.
3.  Blank fields are not permitted. In the example of a preprint/just accepted article, with no page or volume numbers available, do not include these fields. They may be appended at a later date.
4.  Sanitize strings, especially SMILES identifiers, by enclosing them in quotes. `SMILES: '[O][O]'` or `SMILES: 'N#N'` clearly identifies the code as a string, while `SMILES: [O][O]` or `SMILES: N#N` (note the missing quote marks, `'`) will not be identified as strings and will lead to errors.

Thank you
---------
1.  Thank you for taking the time to format your data in an open standard that is both human- and machine-readable.
2.  Thank you for contributing your data to a centralized repository so that is may be easily and freely accessed.

With enough like-minded researchers and contributors, we hope to leverage the enormous potentials of paradigmatic shifts in collaborative frameworks and open science.
