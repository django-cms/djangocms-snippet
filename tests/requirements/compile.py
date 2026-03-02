#!/usr/bin/env python
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

CONFIG_MATRIX = [
    ["python3.10", "Django>=5.2,<6.0", "django-cms>=4.1,<5.0", "py310-django52-cms41.txt",],
    ["python3.10", "Django>=5.2,<6.0", "django-cms>=5.0,<5.1.0a1", "py310-django52-cms50.txt",],

    ["python3.11", "Django>=5.2,<6.0", "django-cms>=4.1,<5.0", "py311-django52-cms41.txt",],
    ["python3.11", "Django>=5.2,<6.0", "django-cms>=5.0,<5.1.0a1", "py311-django52-cms50.txt",],

    ["python3.12", "Django>=5.2,<6.0", "django-cms>=4.1,<5.0", "py312-django52-cms41.txt",],
    ["python3.12", "Django>=5.2,<6.0", "django-cms>=5.0,<5.1.0a1", "py312-django52-cms50.txt",],
    ["python3.12", "Django==6.0", "django-cms>=5.0,<5.1.0a1", "py312-django60-cms50.txt",],

    ["python3.13", "Django>=5.2,<6.0", "django-cms>=5.0,<5.1.0a1", "py313-django52-cms50.txt",],
    ["python3.13", "Django==6.0", "django-cms>=5.0,<5.1.0a1", "py313-django60-cms50.txt",],

]

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    os.environ["CUSTOM_COMPILE_COMMAND"] = "requirements/compile.py"
    os.environ["PIP_REQUIRE_VIRTUALENV"] = "0"
    common_args = [
        "-m",
        "piptools",
        "compile",
        "--generate-hashes",
        "--allow-unsafe",
        *sys.argv[1:],
    ]

    for req in CONFIG_MATRIX:
        cmd = [
            req[0],
            *common_args,
            "--upgrade-package",
            req[1],
            "--upgrade-package",
            req[2],
            "--output-file",
            req[3],
        ]
        print(" ".join(cmd))
        output = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
        )
        print(output.stderr.decode('utf-8'))

