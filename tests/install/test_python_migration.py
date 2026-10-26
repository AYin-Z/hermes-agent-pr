"""Runtime floor decisions for real installer/update compatibility tests."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "python_migration",
    Path(__file__).resolve().parents[2] / "scripts/sandbox/python_migration.py",
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.mark.parametrize("installed, requirement, expected", [
    ("3.11.17", ">=3.14", True),
    ("3.14.0", ">=3.14", False),
    ("3.15.1", ">=3.14", False),
    ("3.14.1", ">=3.14.2", True),
])
def test_runtime_floor(installed, requirement, expected):
    assert module.needs_migration(installed, requirement) is expected


def test_unknown_version_policy_fails_explicitly():
    with pytest.raises(ValueError):
        module.needs_migration("3.11.17", ">=3.14,<3.15")
