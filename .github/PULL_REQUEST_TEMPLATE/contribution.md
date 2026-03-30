---
name: Data Contribution
about: Contribute experimental data (ChemKED YAML or Chemkin kinetic model)
title: "[Contribution] "
labels: contribution
assignees: ''
---

## Contributor Information

**Name:** <!-- Your full name -->
**ORCID:** <!-- Your ORCID iD, e.g., 0000-0003-4425-7097 -->

## Contribution Details

**File type:** <!-- ChemKED YAML / Chemkin kinetic model -->
**Experiment type:** <!-- e.g., ignition delay, laminar burning velocity, etc. -->
**Fuel(s):** <!-- e.g., methane, hydrogen, etc. -->

## Files

<!-- List the files being contributed -->
- 

## Reference

**DOI:** <!-- Required: DOI of the source publication -->
**Journal:** 
**Year:** 

## Description

<!-- Brief description of the data and any relevant notes -->

## Checklist

- [ ] File has at least one `file-author` with a valid ORCID
- [ ] Data validated against PyKED schema (`python scripts/validate_chemked.py <file>`)
- [ ] DOI is permanent and accessible
- [ ] No blank fields (omit if unavailable rather than leaving empty)
- [ ] SMILES strings are properly quoted
- [ ] Composition data uses mole fraction

## Automated Checks

CI will automatically run:
- [ ] **PyKED schema validation** – verifies YAML structure and data types
- [ ] **ORCID check** – confirms contributor identity metadata
- [ ] **PyTeCK simulation** – validates data against kinetic model (if `run-pyteck` label added)
