#!/usr/bin/env python3

import sys
import argparse


# These filenames may only be valid for certain devices
FILE_THRESHOLD_START = r"/sys/class/power_supply/BAT0/charge_control_start_threshold"
FILE_THRESHOLD_END = r"/sys/class/power_supply/BAT0/charge_control_end_threshold"

# The recommanded threshold for taking care of the battery may be different for other devices
PRESET_CARE = [ 40, 50 ] 
PRESET_FULL = [ 80, 100 ]


def _write_threshold(limit: int, file: str):
    with open(file, "w") as fp:
        fp.write(str(limit))


def _read_threshold(file: str) -> int:
    with open(file, "r") as fp:
        return int(fp.read())


def _write_threshold_start(limit: int):
    _write_threshold(limit, FILE_THRESHOLD_START)


def _write_threshold_end(limit: int):
    _write_threshold(limit, FILE_THRESHOLD_END)


def _write_thresholds(start: int, end: int):
    _, curr_end = _read_thresholds()

    if start >= curr_end:
        _write_threshold_end(end)
        _write_threshold_start(start)
    else:
        _write_threshold_start(start)
        _write_threshold_end(end)


def _read_thresholds() -> (int, int):
    return (_read_threshold(FILE_THRESHOLD_START), _read_threshold(FILE_THRESHOLD_END))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set battery charging thresholds. Use either the 'preset' option or any combination of 'start' and 'end'.")

    parser.add_argument("-s", "--start", type=int, help="Threshold when to start charging if below")
    parser.add_argument("-e", "--end", type=int, help="Threshold when to stop charging if above")
    parser.add_argument("-d", "--dump", action='store_true', help="Dump current thresholds")
    parser.add_argument("-p", "--preset", type=str, choices=["full", "care"], help="Select preset: 'full' to charge the battery to 100%%, 'care' to take care of the battery")

    args = parser.parse_args()

    try:
        if args.dump:
            curr_start, curr_end = _read_thresholds()
            print(f"Current thresholds: start={curr_start}%, end={curr_end}%")
            sys.exit(0)

        match (args.start is not None, args.end is not None, args.preset):
            # Preset: full
            case [False, False, 'full']:
                _write_thresholds(PRESET_FULL[0], PRESET_FULL[1])

            # Preset: care
            case [False, False, 'care']:
                _write_thresholds(PRESET_CARE[0], PRESET_CARE[1])

            # Start
            case [True, False, None]:
                _write_threshold_start(int(args.start))

            # End
            case [False, True, None]:
                _write_threshold_end(int(args.end))

            # Start and end
            case [True, True, None]:
                _write_thresholds(int(args.start), int(args.end))

            # Invalid
            case _:
                print("Invalid argument(s). Use either 'preset' with pre-defined values or any combination of 'start' and 'end'.")
                parser.print_help()
                sys.exit(1)

    except Exception as exc:
        print("Failed to perform action.")
        print(exc)
        sys.exit(1)

    sys.exit(0)
