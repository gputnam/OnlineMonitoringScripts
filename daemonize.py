#!/usr/bin/python
# runs a script as a daemon
# if the script fails, waits a second and then restarts
import sys
import os
import time

if __name__ == "__main__":
    script_name = sys.argv[1]
    while True:
        os.system(script_name)
        time.sleep(1)
