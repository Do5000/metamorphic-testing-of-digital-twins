import pytest

def pytest_addoption(parser):
    parser.addoption("--wait-time", action="store", default=30.0, type=float, help="Global wait time in seconds for physical simulation")

def pytest_configure(config):
    """
    Register custom markers for Metamorphic Testing.
    """
    config.addinivalue_line(
        "markers", "mr(type): mark test as a Metamorphic Relation test of a specific type (e.g., monotonicity)"
    )

def pytest_runtest_makereport(item, call):
    """
    Custom reporting hook. Can be used to inject additional MT-specific output.
    """
    # For now, standard pytest reporting is excellent.
    pass
