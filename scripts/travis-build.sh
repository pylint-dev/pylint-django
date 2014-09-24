#!/bin/bash
PYSCR=$(cat <<EOF
import os, sys
for skip_ver in os.environ.get('SKIP', '').split():
    skip_ver = tuple(map(int, skip_ver.split('.')))
    if skip_ver == sys.version_info[:len(skip_ver)]:
        sys.exit(1)
sys.exit(0)
EOF
)

python -c "$PYSCR"

if [ "$?" -eq "0" ]
then
    coverage run test/test_func.py
fi
