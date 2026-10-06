#!/usr/bin/env python3
"""Run with Python 3.11+ from any directory. State stays beside r-place in .rplace-runtime-v43/."""
import sys
from runtime.cli import main
from runtime.common import Error
try:
    result=main()
    if isinstance(result,int): sys.exit(result)
except Error as error:
    print(str(error),file=sys.stderr); sys.exit(2)
