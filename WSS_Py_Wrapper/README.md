# wss-py-wrapper

Python wrapper around a C#/.NET interface (HFI_WSS_Interface) using `pythonnet`.

## Prerequisites

- Python >= 3.9
- A `Cs_Libraries/` folder containing the required `.dll` files

`Cs_Libraries/` must exist at or above the package directory. DLL discovery walks upward looking for `Cs_Libraries/` (see `src/wss_py_wrapper/config.py`).

## Install (dev)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

## Quick Start

Sanity import:

```bash
python -c "import wss_py_wrapper; print('ok')"
```

Run the interactive CLI:

```bash
python -m wss_py_wrapper.cli -- --help
python -m wss_py_wrapper.cli --
```

Run the CLI in simulated transport mode (still requires DLLs):

```bash
python -m wss_py_wrapper.cli -- --test
```

## Library Usage

```python
from pathlib import Path

from wss_py_wrapper import StimulationController, WssConfig


config = WssConfig.default(Path(__file__))
controller = StimulationController(config)
controller.Initialize()

controller.StartStimulation()
controller.StimWithMode("index", 0.25)
controller.StopStimulation()

controller.Shutdown()
```

## Development

Formatting/lint/type-check (optional; not configured in-repo):

```bash
python -m pip install -U ruff mypy
python -m ruff format src
python -m ruff check src
python -m mypy src/wss_py_wrapper
```

Build docs (Sphinx):

```bash
python -m pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
```
