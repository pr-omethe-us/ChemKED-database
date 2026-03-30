#!/usr/bin/env python
"""
Check that ChemKED YAML files include at least one file-author with an ORCID.

Usage:
  - CI mode:  Set CHANGED_FILES env var as a JSON array of paths.
  - CLI mode: python check_orcid.py file1.yaml file2.yaml ...
"""

import json
import os
import re
import sys
import argparse

import yaml


ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


def validate_orcid_format(orcid_str):
    """Check that an ORCID string matches the expected 0000-0000-0000-000X format."""
    return bool(ORCID_PATTERN.match(str(orcid_str).strip()))


def check_file(filepath):
    """Check a single file for ORCID presence and validity.

    Returns (filepath, status, messages) where status is 'pass', 'warn', or 'fail'.
    """
    messages = []
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return (filepath, "fail", [f"Cannot parse YAML: {e}"])

    if not isinstance(data, dict):
        return (filepath, "fail", ["File does not contain a valid YAML mapping"])

    file_authors = data.get("file-authors", [])
    if not file_authors:
        return (filepath, "fail", ["No 'file-authors' field found"])

    has_orcid = False
    for i, author in enumerate(file_authors):
        if not isinstance(author, dict):
            messages.append(f"file-authors[{i}]: not a valid mapping")
            continue

        name = author.get("name", "Unknown")
        orcid = author.get("ORCID")

        if orcid:
            if validate_orcid_format(orcid):
                has_orcid = True
                messages.append(f"{name}: ORCID {orcid} ✓")
            else:
                messages.append(f"{name}: ORCID '{orcid}' has invalid format")
        else:
            messages.append(f"{name}: no ORCID provided")

    if has_orcid:
        return (filepath, "pass", messages)
    else:
        return (filepath, "warn", ["No file-author has a valid ORCID. "
                                   "At least one ORCID is strongly recommended."] + messages)


def collect_files_from_env():
    raw = os.environ.get("CHANGED_FILES", "[]")
    try:
        files = json.loads(raw)
    except json.JSONDecodeError:
        files = []
    return [f for f in files if f.endswith((".yaml", ".yml")) and os.path.isfile(f)]


def main():
    parser = argparse.ArgumentParser(description="Check ORCID in ChemKED file-authors")
    parser.add_argument("files", nargs="*", help="YAML files to check")
    args = parser.parse_args()

    files = args.files if args.files else collect_files_from_env()

    if not files:
        print("No YAML files to check.")
        return

    print(f"Checking ORCID metadata in {len(files)} file(s)...\n")

    passed = 0
    warned = 0
    failed = 0

    for filepath in sorted(files):
        fpath, status, msgs = check_file(filepath)
        label = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[status]
        print(f"  [{label}] {fpath}")
        for m in msgs:
            print(f"         {m}")

        if status == "pass":
            passed += 1
        elif status == "warn":
            warned += 1
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::warning file={fpath}::Missing ORCID in file-authors")
        else:
            failed += 1
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::error file={fpath}::ORCID check failed: {'; '.join(msgs)}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {warned} warnings, {failed} failed")
    print(f"{'='*60}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("## ORCID Metadata Check\n\n")
            f.write(f"**{passed}** with ORCID, **{warned}** missing ORCID (warning), "
                    f"**{failed}** failed\n")

    # Fail only on hard errors; missing ORCID is a warning
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
