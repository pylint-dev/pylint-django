#!/bin/bash

# Build packages for distribution on PyPI
# and execute some sanity scripts on them
#
# note: must be executed from the root directory of the project

# first clean up the local environment
echo "..... Clean up first"
find . -type f -name '*.pyc' -delete
find . -type d -name __pycache__ -delete
find . -type d -name '*.egg-info' | xargs rm -rf
rm -rf build/ .cache/ dist/ .eggs/ .tox/

# check rst formatting of README/CHANGELOG before building the package
echo "..... Check rst formatting for PyPI"
tox -e readme

# then build the packages
echo "..... Building PyPI packages"
set -e
python setup.py sdist >/dev/null
python setup.py bdist_wheel >/dev/null
set +e

# then run some sanity tests
echo "..... Searching for .pyc files inside the built packages"
matched_files=`tar -tvf dist/*.tar.gz | grep -c "\.pyc"`
if [ "$matched_files" -gt "0" ]; then
    echo "ERROR: .pyc files found in .tar.gz package"
    exit 1
fi
matched_files=`unzip -t dist/*.whl | grep -c "\.pyc"`
if [ "$matched_files" -gt "0" ]; then
    echo "ERROR: .pyc files found in wheel package"
    exit 1
fi

echo "..... Trying to verify that all source files are present"
# remove pylint_django/*.egg-info/ generated during build
find . -type d -name '*.egg-info' | xargs rm -rf

source_files=`find ./pylint_django/ -type f | sed 's|./||'`

# verify for .tar.gz package
package_files=`tar -tvf dist/*.tar.gz`
for src_file in $source_files; do
    echo "$package_files" | grep $src_file >/dev/null
    if [ "$?" -ne 0 ]; then
        echo "ERROR: $src_file not found inside tar.gz package"
        exit 1
    fi
done

# verify for wheel package
package_files=`unzip -t dist/*.whl`
for src_file in $source_files; do
    echo "$package_files" | grep $src_file >/dev/null
    if [ "$?" -ne 0 ]; then
        echo "ERROR: $src_file not found inside wheel package"
        exit 1
    fi
done

# exit on error from now on
set -e

echo "..... Trying to install the new tarball inside a virtualenv"
# note: installs with the optional dependency to verify this is still working
virtualenv .venv/test-tarball
source .venv/test-tarball/bin/activate
pip install -f dist/ pylint_django[with_django]
pip freeze | grep Django
deactivate
rm -rf .venv/

echo "..... Trying to install the new wheel inside a virtualenv"
virtualenv .venv/test-wheel
source .venv/test-wheel/bin/activate
pip install pylint-plugin-utils  # because it does not provide a wheel package
pip install --only-binary :all: -f dist/ pylint_django
deactivate
rm -rf .venv/

echo "..... PASS"
