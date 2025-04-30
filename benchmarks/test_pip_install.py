import subprocess
import tempfile
import os
import shutil
import sys

import pytest

@pytest.mark.parametrize("pip_version", [
    "24.2",
    "24.3",
    "25.0",
    "25.1",
])
def test_pip_install_speed(benchmark, pip_version):
    """Benchmark pip install performance for a given version"""
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_dir = os.path.join(tmpdir, "venv")

        # Create virtualenv
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        pip_exe = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")

        # Downgrade pip to target version
        subprocess.run([pip_exe, "install", f"pip=={pip_version}"], check=True)

        # Benchmark install of a moderate package
        def run_install():
            subprocess.run([pip_exe, "install", "requests"], check=True)

        benchmark.name = f"pip-{pip_version}"
        benchmark(run_install)
