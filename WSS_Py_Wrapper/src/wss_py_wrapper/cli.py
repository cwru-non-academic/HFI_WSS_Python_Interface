"""Interactive console for driving the stimulation controller.

Run via ``python -m wss_py_wrapper.cli -- [options]``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from dataclasses import replace

from .config import WssConfig
from .stimulation_controller import StimulationController


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--serial", dest="serial", help="Fully qualified serial device (auto-detect).")
    parser.add_argument("--config", dest="config", help="Config directory path.")
    parser.add_argument("--max-retries", dest="max_retries", type=int, default=5)
    parser.add_argument("--tick", dest="tick", type=int, default=10)
    parser.add_argument("--test", dest="test_mode", action="store_true")
    parser.add_argument("--help", "-h", action="store_true")
    return parser


def _print_cli_usage() -> None:
    print("HFI WSS Stim console")
    print("Usage: python -m wss_py_wrapper.cli -- [options]")
    print("Options (defaults in parentheses):")
    print("  --serial=NAME       Fully qualified serial device (auto-detect).")
    print("  --config=PATH       Config directory path (./Config).")
    print("  --max-retries=N     Max setup retries (5).")
    print("  --tick=MS           Tick interval in milliseconds (10).")
    print("  --test              Enable simulated transport (off).")
    print("  --help              Show this message.")


def _print_command_help() -> None:
    print("Commands:")
    print("  help                Show this help text.")
    print("  start               Broadcast StartStim.")
    print("  stop                Broadcast StopStim.")
    print("  stim <finger> <v>  Stim with model/params layer (normalized magnitude).")
    print("  analog <finger> <pw> [amp] [ipi]  Send direct analog request.")
    print("  reload-core         Reload the core config JSON.")
    print("  reload-params [p]   Reload params JSON (optionally from path).")
    print("  save-params         Persist params JSON.")
    print("  status              Print Ready/Started/mode state.")
    print("  quit|exit           Terminate the program.")


def _run_interactive_loop(controller: StimulationController) -> None:
    running = True

    try:
        while running:
            try:
                raw = input("> ").strip()
            except EOFError:
                break

            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()

            try:
                if cmd == "help":
                    _print_command_help()
                elif cmd in ("quit", "exit"):
                    running = False
                elif cmd == "start":
                    controller.StartStimulation()
                    print("Stim start requested.")
                elif cmd == "stop":
                    controller.StopStimulation()
                    print("Stim stop requested.")
                elif cmd == "status":
                    print(
                        f"Ready={controller.Ready()}, Started={controller.Started()}, "
                        f"ModeValid={controller.isModeValid()}, BasicSupported={controller.BasicSupported}"
                    )
                elif cmd == "reload-core":
                    controller.LoadCoreConfigFile()
                    print("Core config reloaded.")
                elif cmd == "reload-params":
                    if len(parts) > 1:
                        controller.LoadParamsJson(parts[1])
                    else:
                        controller.LoadParamsJson()
                    print("Params reloaded.")
                elif cmd == "save-params":
                    controller.SaveParamsJson()
                    print("Params saved.")
                elif cmd == "stim":
                    if len(parts) < 3:
                        print("Usage: stim <finger|chX> <magnitude>")
                        continue
                    magnitude = float(parts[2])
                    controller.StimWithMode(parts[1], magnitude)
                elif cmd == "analog":
                    if len(parts) < 3:
                        print("Usage: analog <finger|chX> <pw> [amp] [ipi]")
                        continue
                    pw = int(parts[2])
                    amp = int(parts[3]) if len(parts) > 3 else 3
                    ipi = int(parts[4]) if len(parts) > 4 else 10
                    controller.StimulateAnalog(parts[1], pw, amp, ipi)
                else:
                    print("Unknown command. Type 'help' to list options.")
            except Exception as ex:
                print(f"Command failed: {ex}")
    finally:
        controller.StopStimulation()
        controller.Shutdown()


def main(argv: list[str] | None = None) -> int:
    """Run the interactive CLI.

    :param argv: Optional argument list. If omitted, uses ``sys.argv[1:]``.
    :returns: Process exit code.
    """
    argv = list(argv) if argv is not None else sys.argv[1:]
    if "/?" in argv:
        _print_cli_usage()
        return 0

    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.help:
        _print_cli_usage()
        return 0

    config = WssConfig.default(Path(__file__))
    if args.serial:
        config = replace(config, serial_port=args.serial)
    if args.config:
        config_path = Path(args.config).expanduser().resolve()
        config = replace(config, config_path=config_path)
    if args.max_retries and args.max_retries > 0:
        config = replace(config, max_setup_tries=args.max_retries)
    if args.tick and args.tick > 0:
        config = replace(config, tick_interval_ms=args.tick)
    if args.test_mode:
        config = replace(config, test_mode=True)

    config.config_path.mkdir(parents=True, exist_ok=True)

    controller = StimulationController(config)
    controller.Initialize()
    print("HFI WSS stimulation controller ready.")
    print(f"Config: {config.config_path}")
    print(f"Serial: {config.serial_port or 'auto-detect'}")
    print(
        f"Mode valid: {controller.isModeValid()}, Ready: {controller.Ready()}, Basic API: {controller.BasicSupported}"
    )
    _print_command_help()
    _run_interactive_loop(controller)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
