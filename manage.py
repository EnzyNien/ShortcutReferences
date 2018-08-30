#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "ShortcutReferences.settings"
    )
    
    from django.core.management import execute_from_command_line

    start_param = sys.argv
    start_param = start_param[:-1]
    start_param.append("5555")
    execute_from_command_line(start_param)

