#!/bin/bash
python scripts/travis_skip.py

if [ "$?" -eq "0" ]
then
    pip install --use-mirrors coverage coveralls
    pip install --use-mirrors $DJANGO
    pip install --use-mirrors git+https://github.com/landscapeio/pylint-plugin-utils.git@develop
    pip install --use-mirrors --editable .
else
    echo "Skipping"
fi
