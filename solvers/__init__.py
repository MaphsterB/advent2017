#!/usr/bin/env python
"""
Package containing all the solvers.
"""

ADVENT_DAYS = 25

import re
import os
import os.path

__all__ = ["ADVENT_DAYS"] + \
    [
        os.path.basename(f)[:-3] 
            for f in os.listdir(os.path.dirname(__file__))
            if re.fullmatch(r"day\d+\.py", f)
    ]
