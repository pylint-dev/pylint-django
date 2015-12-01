#!/bin/bash
python scripts/travis-skip.py

if [ "$?" -eq "0" ]
then
    pip install coverage coveralls
    pip install $DJANGO
    pip install git+https://github.com/landscapeio/pylint-plugin-utils.git@develop
    pip install --editable .
else
    echo "Skipping"
fi
