#!/bin/bash
set -e

# Setup venv for testing framework
python3 -m venv .benchenv
source .benchenv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Run the benchmark
pytest benchmarks/test_pip_install.py --benchmark-autosave

# Compare results (optional)
pytest-benchmark compare
