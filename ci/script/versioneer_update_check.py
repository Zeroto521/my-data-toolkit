import os
import sys

try:
    sys.path = sys.path[1:]  # import from the system instead of local
    from versioneer import newver
except:
    sys.exit()


FILE = "versioneer.py"

if not os.path.exists(FILE):
    sys.exit()

for line in open(FILE).readlines()[:5]:
    if "Version" in line and newver in line:  # don't need to update versioneer
        print(True)
        sys.exit()
