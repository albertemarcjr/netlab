"""Exercise checker: run a function against known cases and report, never crash."""

import math


def _same(got, expected):
    """Equal, with a small tolerance for floats (0.1 + 0.2 is not exactly 0.3)."""
    if isinstance(got, float) or isinstance(expected, float):
        try:
            return math.isclose(got, expected, rel_tol=1e-9, abs_tol=1e-9)
        except TypeError:
            return False
    return got == expected


def check(fn, cases, *, name=None) -> bool:
    """Run fn against cases and print one line per case. Never raises.

    cases: list of (args, expected). args is a tuple of positional arguments.
    Prints PASS, FAIL, ERROR, or NOT YET (fn raised NotImplementedError).
    Ends with a summary line. Returns True only if every case passes.
    """
    name = name or getattr(fn, "__name__", "check")
    passed = 0
    for args, expected in cases:
        try:
            got = fn(*args)
        except NotImplementedError:
            print(f"{name}: NOT YET")
            return False
        except Exception as e:  # report any other error as data, don't crash
            print(f"ERROR  args={args!r} {type(e).__name__}: {e}")
            continue
        if _same(got, expected):
            passed += 1
            print("PASS")
        else:
            print(f"FAIL   args={args!r} got={got!r} expected={expected!r}")
    print(f"{name}: {passed}/{len(cases)} passing")
    return passed == len(cases)
