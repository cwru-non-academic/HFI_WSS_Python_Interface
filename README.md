
# WSS Py Wrapper

Python wrapper for the HFI_WSS_Interface library.

## Quick start (Linux)

1) Ensure the C# DLLs are present:

```
../Cs_Libraries/WSS_Core_Interface.dll
```

You can find them in HFI_WSS_Interface: https://github.com/cwru-non-academic/WSSCoreInterface/releases

2) Install venv + Mono, create the environment, and install the package:

```
sudo apt update
sudo apt install python3.10-venv mono-complete

cd .../WSS_Python_Wrapper/WSS_Py_Wrapper
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

3) Run the CLI:

```
python -m wss_py_wrapper.cli --help
python -m wss_py_wrapper.cli --test
```

## Quick start (no install)

```
cd .../WSS_Python_Wrapper
python3.10 -m venv WSS_Py_Wrapper/.venv
source WSS_Py_Wrapper/.venv/bin/activate
python -m pip install -U pip
python -m pip install -e WSS_Py_Wrapper

PYTHONPATH=./WSS_Py_Wrapper/src python -m wss_py_wrapper.cli --test
```

## CLI usage

Run:

```
python -m wss_py_wrapper.cli -- [options]
```

Options:
- `--serial=NAME` Fully qualified serial device (auto-detect if omitted).
- `--config=PATH` Config directory path (defaults to `./Config` under your current working directory).
- `--max-retries=N` Max setup retries (default `5`).
- `--tick=MS` Tick interval in milliseconds (default `10`).
- `--test` Enable simulated transport.
- `--help` Show usage.

Interactive commands:
- `help`, `start`, `stop`, `status`, `quit`/`exit`
- `stim <finger|chX> <magnitude>`
- `analog <finger|chX> <pw> [amp] [ipi]`
- `reload-core`, `reload-params [path]`, `save-params`

## Logging

Console output:
- Startup status (config path, serial selection, readiness).
- Command responses and errors from the interactive loop.

Log file output:
- C# log messages routed via `Log.SetSink(...)` into a file.
- Each line is timestamped: `[YYYY-MM-DD HH:MM:SS] LEVEL: message`.

Default log file location:
- A file named like `wss_YYYYMMDD_HHMMSS.log` alongside the Python module:
  `WSS_Py_Wrapper/src/wss_py_wrapper/wss_YYYYMMDD_HHMMSS.log`

Change log file location:
- Edit `WSS_Py_Wrapper/src/wss_py_wrapper/config.py` and update `WssConfig.default()` to set a different `log_path`.
- Or construct `WssConfig` yourself and pass it to `StimulationController` in your own script.

## Development

Create a virtual environment, then install dependencies:

```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -e .
```
