import sys
import re

for line in sys.stdin:
    line = re.sub('\D', '', line)
    print(line)
