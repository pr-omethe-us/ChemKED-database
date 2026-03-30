#!/usr/bin/env python
"""
Validate ChemKED YAML files using PyKED schema validation.

Usage:
  - CI mode:  Set CHANGED_FILES env var as a JSON array of paths.
  - CLI mode: python validate_chemked.py file1.yaml file2.yaml ...
              python validate_chemked.py --all   (validate entire repo)
"""

import json
import os
import sys
import glob
import argparse
from pathlib import Path


def validate_file(filepath):
    """Validate a single ChemKED YAML file.

    Returns (filepath, success, message) tuple.
    """
    from pyked.chemked import ChemKED

    try:
        ck = ChemKED(filepath)
        n_dp = len(ck.datapoints)
        return (filepath, True, f"OK – {n_dp} datapoint(s)")
    except Exception as e:
        return (filepath, False, str(e))


def collect_files_from_env():
    """Read the list of changed files from the CHANGED_FILES env variable (JSON array)."""
    raw = os.environ.get("CHANGED_FILES", "[]")
    try:
        files = json.loads(raw)
    except json.JSONDecodeError:
        files = []
    return [f for f in files if f.endswith((".yaml", ".yml")) and os.path.isfile(f)]


def collect_all_yaml(root="."):
    """Find all YAML files in the repository."""
    patterns = ["**/*.yaml", "**/*.yml"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(root, pat), recursive=True))
    # Exclude hidden dirs, scripts dir, CI configs
    return [
        f for f in files
        if not any(part.startswith(".") for part in Path(f).parts)
        and "scripts/" not in f
        and "environment" not in os.path.basename(f).lower()
    ]


def main():
    parser = argparse.ArgumentParser(description="Validate ChemKED YAML files")
    parser.add_argument("files", nargs="*", help="YAML files to validate")
    parser.add_argument("--all", action="store_true", help="Validate all YAML files in repo")
    args = parser.parse_args()

    # Determine which files to validate
    if args.files:
        files = [f for f in args.files if os.path.isfile(f)]
    elif args.all:
        files = collect_all_yaml()
    else:
        files = collect_files_from_env()

    if not files:
        print("No YAML files to validate.")
        return

    print(f"Validating {len(files)} file(s)...\n")

    passed = 0
    failed = 0
    results = []

    for filepath in sorted(files):
        fpath, ok, msg = validate_file(filepath)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {fpath}")
        if not ok:
            print(f"         {msg}")
            failed += 1
            # GitHub Actions annotation
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::error file={fpath}::PyKED validation failed: {msg}")
        else:
            passed += 1
        results.append({"file": fpath, "status": status, "message": msg})

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(files)} file(s)")
    print(f"{'='*60}")

    # Write a summary for GitHub Actions step summary
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("## PyKED Schema Validation\n\n")
            f.write(f"| Status | File | Details |\n")
            f.write(f"|--------|------|---------|\n")
            for r in results:
                icon = "✅" if r["status"] == "PASS" else "❌"
                f.write(f"| {icon} | `{r['file']}` | {r['message']} |\n")
            f.write(f"\n**{passed}** passed, **{failed}** failed\n")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
