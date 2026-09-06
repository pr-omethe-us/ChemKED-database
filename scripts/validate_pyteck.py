#!/usr/bin/env python
"""
Run PyTeCK simulation smoke-test against contributed ChemKED files.

Only processes ignition delay datasets (the primary experiment type supported
by PyTeCK). Other experiment types are skipped with a note.

Usage:
  - CI mode:  Set CHANGED_FILES env var as a JSON array of paths.
  - CLI mode: python validate_pyteck.py --model model.yaml --spec-keys keys.yaml file1.yaml ...

Environment variables:
  PYTECK_MODEL       – Path to kinetic model file (Cantera YAML / CTI)
  PYTECK_SPEC_KEYS   – Path to species key mapping YAML
  CHANGED_FILES      – JSON array of files (CI mode)
"""

import json
import os
import sys
import argparse
import tempfile

import yaml


SUPPORTED_EXPERIMENT_TYPES = {"ignition delay"}


def check_experiment_type(filepath):
    """Return the experiment-type from a ChemKED file without importing PyKED."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return data.get("experiment-type", "").lower().strip()


def run_pyteck_on_file(filepath, model_file, spec_keys_file):
    """Run PyTeCK evaluation on a single ChemKED dataset.

    Returns (filepath, success, message).
    """
    from pyteck.eval_model import evaluate_model

    exp_type = check_experiment_type(filepath)
    if exp_type not in SUPPORTED_EXPERIMENT_TYPES:
        return (filepath, True, f"Skipped – experiment type '{exp_type}' not simulated by PyTeCK")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Write a dataset list file pointing to our single file
        dataset_list = os.path.join(tmpdir, "datasets.txt")
        with open(dataset_list, "w") as f:
            f.write(os.path.basename(filepath) + "\n")

        results_path = os.path.join(tmpdir, "results")
        data_path = os.path.dirname(os.path.abspath(filepath))

        try:
            output = evaluate_model(
                model_name=model_file,
                spec_keys_file=spec_keys_file,
                dataset_file=dataset_list,
                data_path=data_path,
                results_path=results_path,
                num_threads=1,
                skip_validation=False,
            )

            # Extract error metric
            datasets = output.get("datasets", [])
            if datasets:
                error = datasets[0].get("error_func", float("nan"))
                msg = f"Simulation OK – error function = {error:.4f}"
            else:
                msg = "Simulation completed but no output datasets"

            return (filepath, True, msg)

        except Exception as e:
            return (filepath, False, f"Simulation failed: {e}")


def collect_files_from_env():
    raw = os.environ.get("CHANGED_FILES", "[]")
    try:
        files = json.loads(raw)
    except json.JSONDecodeError:
        files = []
    return [f for f in files if f.endswith((".yaml", ".yml")) and os.path.isfile(f)]


def main():
    parser = argparse.ArgumentParser(description="PyTeCK simulation validation")
    parser.add_argument("files", nargs="*", help="ChemKED YAML files")
    parser.add_argument("--model", default=os.environ.get("PYTECK_MODEL", ""),
                        help="Path to kinetic model file")
    parser.add_argument("--spec-keys", default=os.environ.get("PYTECK_SPEC_KEYS", ""),
                        help="Path to species key mapping YAML")
    args = parser.parse_args()

    files = args.files if args.files else collect_files_from_env()

    if not files:
        print("No YAML files to validate with PyTeCK.")
        return

    if not args.model or not args.spec_keys:
        print("PyTeCK validation requires --model and --spec-keys (or env PYTECK_MODEL / PYTECK_SPEC_KEYS).")
        print("Skipping simulation validation.")
        return

    print(f"Running PyTeCK simulation on {len(files)} file(s)...\n")

    passed = 0
    failed = 0

    for filepath in sorted(files):
        fpath, ok, msg = run_pyteck_on_file(filepath, args.model, args.spec_keys)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {fpath}")
        print(f"         {msg}")

        if ok:
            passed += 1
        else:
            failed += 1
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::error file={fpath}::PyTeCK validation failed: {msg}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(files)} file(s)")
    print(f"{'='*60}")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("## PyTeCK Simulation Validation\n\n")
            f.write(f"**{passed}** passed, **{failed}** failed\n")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
