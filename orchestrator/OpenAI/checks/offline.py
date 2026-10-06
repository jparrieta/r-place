"""Run the Codex offline suite on the local Python 3.11 environment, without model calls."""
from pathlib import Path
import os
import subprocess

repo = Path(__file__).resolve().parents[3]
python = repo.parent / '.rplace-runtime/tools/python311/venv/bin/python3'
if not python.is_file():
    raise SystemExit('Python 3.11 environment missing: see OpenAI/README.md. Do not lower the reserve or use a shim.')
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
probe = subprocess.run([str(python), '-c',
    'import sys,numpy,scipy; assert sys.version_info[:2] == (3,11); '
    'print("Python",sys.version.split()[0],"NumPy",numpy.__version__,"SciPy",scipy.__version__)'], env=env)
if probe.returncode:
    raise SystemExit(probe.returncode)
raise SystemExit(subprocess.run(
    [str(python), '-m', 'unittest', 'discover', '-s', 'runtime/tests'],
    cwd=repo / 'aggregator/handler/codex', env=env).returncode)
