"""The upgrade bootstrap must load before new application dependencies exist."""
import subprocess
import sys
from pathlib import Path


def test_managed_uv_import_without_site_packages(tmp_path):
    result = subprocess.run(
        [sys.executable, "-S", "-c", (
            "import sys; import hermes_cli.managed_uv; "
            "assert 'tools.environments.base' not in sys.modules; "
            "assert 'orjson' not in sys.modules"
        )],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
