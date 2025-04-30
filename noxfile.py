import nox

nox.options.reuse_existing_virtualenvs = True

@nox.session
def tests(session):
    """Run benchmarks."""
    session.install("pytest", "pytest-benchmark")
    session.run("pytest", "benchmarks/test_pip_install.py", "--benchmark-autosave")
    session.run("pytest-benchmark", "compare")
