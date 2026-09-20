"""Enable `python -m requirements_quality_assessment`."""

import sys

from .cli import main

if __name__ == "__main__":
    # A Windows process launched with redirected output may default to cp1252.
    # Preserve Ukrainian source text in the approved console report and errors.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
