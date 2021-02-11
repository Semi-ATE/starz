#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License

import os
import sys
import ast
import shutil
import fnmatch
import site
import glob

from setuptools import setup, find_packages

from setuptools import Command
class clean(Command):
    """Custom clean command to tidy up the project root."""
    DIRS_TO_CLEAN = ["./build",  "./dist", "./*.pyc", "./starz/__pycache__", "./*.egg-info", "./.pytest_cache"]
    FILES_TO_CLEAN = [".coverage"]

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        global here

        for DIR_TO_CLEAN in self.DIRS_TO_CLEAN:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(os.path.join(here, DIR_TO_CLEAN)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError(f"{path} is not a path inside {here}")
                print(f"removing directory '{os.path.relpath(path)}' ... ", end="")
                shutil.rmtree(path)
                print("Done.")
        for FILE_TO_CLEAN in self.FILES_TO_CLEAN:
            abs_path = os.path.normpath(os.path.join(here, FILE_TO_CLEAN))
            if os.path.exists(abs_path):
                print(f"removing file '{FILE_TO_CLEAN}' ... ", end="")
                os.remove(abs_path)
                print("Done.")

from setuptools.command.develop import develop as develop_base
class develop(develop_base):
    """Custom develop with post-develop-installation stuff"""
    def run(self):
        develop_base.run(self)
        # custom post develop-install stuff comes here

from setuptools.command.install import install as install_base
class install(install_base):
    """Custom install with post-installation stuff"""
    def run(self):
        install_base.run(self)
        # custom post-install stuff comes here

here = os.path.dirname(os.path.abspath(__file__))
Project_name = "starz"
Project_root = os.path.join(here, Project_name)
project_main = os.path.join(Project_root, "__main__.py")
Project_init = os.path.join(Project_root, "__init__.py")
from starz.__init__ import __version__ as Project_version

with open(os.path.join(here, "README.md"), "r") as f:
    Project_description = f.read()

PyMajor = sys.version_info.major
PyMinor = sys.version_info.minor
PyMicro = sys.version_info.micro
PyVersion = f"{PyMajor}.{PyMinor}.{PyMicro}"

if PyMajor < 3:
    print(f"Python 3 is required, but we detected Python {PyVersion}.")
    sys.exit(1)

if PyMinor < 7:
    print(f"Python 3.7+ is required, but we detected Python {PyVersion}.")
    sys.exit(1)


# https://setuptools.readthedocs.io/en/latest/
setup(
    name=Project_name,
    version=Project_version,
    description='Sized Tape ARchiveZ',
    long_description=Project_description,
    long_description_content_type='text/markdown',
    author='Tom Hören',
    author_email='horen.tom@gmail.com',
    maintainer='Semi-ATE',  # supperseeds author !
    maintainer_email='info@Semi-ATE.com',  # the Semi-ATE official e-mail address
    url='https://github.com/Semi-ATE/starz',
    packages=find_packages(),
    cmdclass={
        'develop': develop,
        'install': install,
        'clean': clean,
    },
#    scripts=[],
    classifiers=[  # https://pypi.org/classifiers/
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
    ],
    license="MIT",
    keywords=[  # PEP-314 : https://www.python.org/dev/peps/pep-0314/
        'tar',
        'archives',
        'docker',
        'vivado',
        'petalinux',
    ],
    platforms=['noarch'],
#    zip_safe=True,  # TODO: maybe set to False, so that only wheel packages are made ?
#    install_requires=[],  # TODO: How do I get requirements/run.txt in here ?!?
#    setup_requires=[],  # usage discouraged in favor of PEP-518 : https://www.python.org/dev/peps/pep-0518/
    python_requires='>=3.7', # PEP 440 : https://www.python.org/dev/peps/pep-0440/ 

)
