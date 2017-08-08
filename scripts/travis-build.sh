#!/bin/bash
python scripts/travis_skip.py

if [ "$?" -eq "0" ]
then
    coverage run -m test.test_func
else
    echo "Skipping"
fi
