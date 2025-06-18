PYTHON PACKAGING

pip
PyPI
pip installs all dependencies 
sdist (source dist) (tarball tar.gz)
wheel (pre-compiled binary .whl zip)

alternative:
- PEX (subpar, shiv, zipapp) turn python into one file (still needs Python installed)
- PyInstaller, PyOxidizer turn python into executable (Python included)
- Linux package RPM / DEB
- Docker container
- Conda (pip+OS, but only works w Anaconda Python)

PyPI package build tool:
- setuptools, flit, poetry (don't use obsolete distutils)

project/
├── LICENSE.txt
├── pyproject.toml
├── README.md (or txt)
├── CHANGES.txt
├── setup.py
├── setup.cfg
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
└── docs/
└── dist/


cd same directory as pyproject.toml
--- MAKE sdist
python setup.py check
python setup.py sdist

--- MAKE wheel
pip install wheel
python setup.py bdist_wheel --universal
?OR?
python3 -m pip install --upgrade build (aka pip install --upgrade build)
python3 -m build # CREATES: dist/ with .tar.gz and .whl

# upload to test.pypi.org
pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

# USERS INSTALL WITH:
pip install --index-url https://test.pypi.org/simple/ --no-deps mypackage

# test it! Then upload to real pypi
# create pypi account
twine upload dist/*
pip install mypackage

----------
# pyproject.toml
[build-system]
requires = ['setuptools>=42']
build-backend = 'setuptools.build_meta'

-----------
# setup.py
import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "package-name",
    version = "0.0.1",
    author = "author",
    author_email = "author@example.com",
    description = "short package description",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "package URL",
    project_urls = {
        "Bug Tracker": "package issues URL",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)

-----------
# __init__.py
""" documentation """
__version__ = "0.1.0"
__author__ = 'Stephen Hudson'
__credits__ = 'Argonne National Laboratory'

-------------
# setup.cfg
[metadata]
name = package-name
version = 0.0.1
author = name of the author
author_email = author@example.com
description = short package description
long_description = file: README.md
long_description_content_type = text/markdown
url = package url
project_urls =
    Bug Tracker = package issues url
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.6

[options.packages.find]
where = src

---------------
# sample test
import unittest
from divide.by_three import divide_by_three 

class TestDivideByThree(unittest.TestCase):

  def test_divide_by_three(self):
    self.assertEqual(divide_by_three(12), 4)

unittest.main()
