#!/usr/bin/env python
import os
import sys
for skip_ver in os.environ.get('SKIP', '').split():
    skip_ver = tuple(map(int, skip_ver.split('.')))
    if skip_ver == sys.version_info[:len(skip_ver)]:
        sys.exit(1)
sys.exit(0)
