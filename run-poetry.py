# save as export_reqs.py  (or just paste into a notebook / REPL)
import sys, re, pathlib, tomllib  # tomllib is built‑in from Python 3.11+
from typing import Iterable

def main(lock_path: str = "poetry.lock", out_path: str = "requirements.txt") -> None:
    lock = tomllib.loads(pathlib.Path(lock_path).read_text())
    req_lines: list[str] = []

    for section in lock.get("package", []):
        if "main" not in section.get("groups", []):
            continue                       # skip dev / docs / test extras
        name  = section["name"]
        ver   = section["version"]
        # pin strictly: name==x.y.z
        req_lines.append(f"{name}=={ver}")

    req_lines.sort(key=str.lower)
    pathlib.Path(out_path).write_text("\n".join(req_lines) + "\n")
    print(f"Wrote {len(req_lines)} lines to {out_path}")

if __name__ == "__main__":
    main(*sys.argv[1:])   # allow custom paths if you want
