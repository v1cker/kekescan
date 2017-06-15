#!/usr/bin/env python
# -*- coding: utf-8 -*-  


"""
Command-line utility for administrative tasks.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "xlcscan.settings"
    )


    from django.core.management import execute_from_command_line

    import thread
    from taskmanager import task_sched
    from httpmonitor import sql_sched
 
    for arg in sys.argv:
        if 'runserver' in arg:
            thread.start_new_thread(task_sched, ())
            thread.start_new_thread(sql_sched, ())

    execute_from_command_line(sys.argv)
