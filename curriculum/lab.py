"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")




def run():
    from dynamics_topology.analysis import analyze
    def model(a, d, b="0"):
        return {"schema_version":1,"matrix":[[a,b],["0",d]],"initial":["1","1"],"steps":2}
    r = analyze(model("1/2","1/2"))
    check("strict Schur stability", r["classification"], "SCHUR_STABLE")
    check("exact trajectory", r["trajectory"], [["1","1"],["1/2","1/2"],["1/4","1/4"]])
    check("Lyapunov solution for A=I/2", r["lyapunov_certificate"]["matrix"], [["4/3","0"],["0","4/3"]])
    check("exact residual", r["lyapunov_certificate"]["equation_residual"], ["0","0","0"])
    check("identity is boundary, not strict stability", analyze(model("1","1"))["classification"], "CRITICAL_OR_NONDECAYING")
    j = analyze(model("1","1","1"))
    check("Jordan boundary can grow", j["trajectory"][-1], ["3","1"])
    check("unstable diagonal", analyze(model("2","1/2"))["classification"], "UNSTABLE")
    rejects("floating coefficients rejected", lambda: analyze(model(.5,"1/2")))

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
