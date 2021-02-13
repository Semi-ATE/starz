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
    items_to_clean = [
        './build',
        './dist',
        '*__pycache__',
        "*.pytest_cache"
        '*~',
        '*.egg-info',
        '*#*#',
        '*#',
        ".coverage",
    ]

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        home = os.getcwd()
        for Root, Dirs, Files in os.walk(home):
            for File in Files:
                abs_path = os.path.join(Root, File)
                rel_path = abs_path.replace(home, '.')
                for item_to_clean in self.items_to_clean:
                    if fnmatch.fnmatch(rel_path, item_to_clean):
                        print(f"  deleting file '{rel_path}' ... ", end='')
                        os.unlink(abs_path)
                        print("Done.")
            for Dir in Dirs:
                abs_path = os.path.join(Root, Dir)
                rel_path = abs_path.replace(home, '.')
                for item_to_clean in self.items_to_clean:
                    if fnmatch.fnmatch(rel_path, item_to_clean):
                        print(f"  deleting directory '{rel_path}' ... ", end='')
                        shutil.rmtree(abs_path)
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


with open(os.path.join(here, "requirements", "run.txt"), "r") as requirements:
    run_requirements = requirements.readlines()
install_requirements = []
for requirement in run_requirements:
    if requirement.replace("\n", "") != "":
        install_requirements.append(requirement.replace("\n", ""))

# https://setuptools.readthedocs.io/en/latest/
# PEP-314 (Metadata for Python Software Packages) : https://www.python.org/dev/peps/pep-0314/
# https://pypi.org/classifiers/
setup(
    name=Project_name,
    version=Project_version,
    description='Sized Tape ARchiveZ',
    long_description=Project_description,
    long_description_content_type='text/markdown',
    author='Tom Hören',
    maintainer='Semi-ATE',
    maintainer_email='info@Semi-ATE.com',
    url='https://github.com/Semi-ATE/starz',
    packages=find_packages(),
    cmdclass={
        'develop': develop,
        'install': install,
        'clean': clean,
    },
    entry_points={
        'console_scripts': [
            'starz=starz.__main__:main',
            ],
    },
#    scripts=[],
    classifiers=[  
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
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
    keywords=[  
        'tar',
        'archives',
        'docker',
        'vivado',
        'petalinux',
    ],
    platforms=["Windows", "Linux", "MacOS"],
    install_requires=install_requirements,
    python_requires='>=3.7',
)
