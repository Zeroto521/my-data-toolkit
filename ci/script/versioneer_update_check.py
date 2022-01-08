import os
import sys


if os.path.exists("versioneer.py"):
    try:
        sys.path = sys.path[1:]  # import from the system instead of local
        from versioneer import newver
    except:
        sys.exit()

    for line in open("versioneer.py").readlines()[:5]:
        if "Version" in line and newver in line:  # don't need to update versioneer
            print(True)
            sys.exit()
