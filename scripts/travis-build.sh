#!/bin/bash
python scripts/travis-skip.py

if [ "$?" -eq "0" ]
then
    coverage run test/test_func.py
else
    echo "Skipping"
fi
