# starz
**S**ized **T**ape **AR**chive**Z**

[![GitHub](https://img.shields.io/github/license/Semi-ATE/starz?color=black)](https://github.com/Semi-ATE/starz/blob/main/LICENSE) 
![Conda](https://img.shields.io/conda/pn/conda-forge/starz?color=black)
![Supported Python versions](https://img.shields.io/badge/python-%3E%3D3.7-black)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

[![CI](https://github.com/Semi-ATE/starz/workflows/CI/badge.svg?branch=main)](https://github.com/Semi-ATE/starz/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/Semi-ATE/starz/branch/main/graph/badge.svg)](https://codecov.io/gh/Semi-ATE/starz)
[![CD](https://github.com/Semi-ATE/starz/workflows/CD/badge.svg)](https://github.com/Semi-ATE/starz/actions?query=workflow%3ACD)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/starz?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/starz/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/starz/latest)](https://github.com/Semi-ATE/starz)
[![PyPI](https://img.shields.io/pypi/v/starz?color=blue&label=PyPI)](https://pypi.org/project/starz/)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/starz?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/starz)
[![conda-forge feedstock](https://img.shields.io/github/issues-pr/conda-forge/starz-feedstock?label=feedstock)](https://github.com/conda-forge/starz-feedstock)

![PyPI - Downloads](https://img.shields.io/pypi/dm/starz?color=g&label=PyPI%20downloads)
![Conda](https://img.shields.io/conda/dn/conda-forge/starz?color=g&label=conda-forge%20downloads)

[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/starz)](https://github.com/Semi-ATE/starz/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/starz)](https://github.com/Semi-ATE/starz/pulls)

This small command line tool creates sized (gzipped) tar files from either a (gzipped) tar or a directory.

The 'raison d'être' of this tool is because [GitHub Packages](https://github.com/features/packages) limits the layer size of a docker container to 5GB.
This poses a problem when one needs to install huge tarballs (eg: [PetaLinux](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html), [vivado](https://www.xilinx.com/support/download.html), ...)

The Unix [split](https://www.man7.org/linux/man-pages/man1/split.1.html) command will **not** do as each resulting 'split' is not individual un-tar-able, and after a [cat](https://www.man7.org/linux/man-pages/man1/cat.1.html) of the individual parts, we violate the 5GB layer constraint again.
 
# Installation

## conda

```sh
(conda-forge) me@mybox$ conda install starz
```

## pip

```sh
me@mybox$ pip install starz
Collecting starz
  Downloading starz-0.2.1.tar.gz (9.1 kB)
Collecting tqdm
  Downloading tqdm-4.56.2-py2.py3-none-any.whl (72 kB)
     |████████████████████████████████| 72 kB 569 kB/s 
Collecting filetype
  Downloading filetype-1.0.7-py2.py3-none-any.whl (15 kB)
Building wheels for collected packages: starz
  Building wheel for starz (setup.py) ... done
  Created wheel for starz: ...
  Stored in directory: ...
Successfully built starz
Installing collected packages: tqdm, filetype, starz
Successfully installed filetype-1.0.7 starz-0.2.1 tqdm-4.56.2
me@mybox:~$ 
```

# Usage

```bash
me@mybox$ starz --help
usage: starz [-h] -s SIZE [-c] [-q] [-v] SOURCE [DESTINATION]

Pack a directory or re-pack a .tag(.gz) file in smaller .tar(.gz) chunks.

positional arguments:
  SOURCE                path to either a .tar(.gz) file or a directory
  DESTINATION           destination directory (default is current working
                        directory)

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  maximum size (eg. 5GB or 3.14MB)
  -c, --compress        compress (gzip) the resulting .tar files into .tar.gz
  -q, --quiet           surpress the progress bar
  -v, --version         print the version number
me@mybox$
```

re-packing a big gzipped-tar file in smaller non-compressed tar files :

```bash
me@mybox$ starz -s 15MB brol.tar.gz
brol.00.tar:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```

re-packing a big gzipped-tar file in smaller gzipped-tar files :

```bash
me@mybox$ starz -c -s 15MB brol.tar.gz
brol.00.tar.gz:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar.gz:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar.gz:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```

same as above, but not outputting progress bar :

```bash
me@mybox$ starz -q -c -s 15MB brol.tar.gz
me@mybox$ 
```

packing the `./brol` directory (recursively) in compressed-tar files with less than 15MB of content each:

```bash
me@mybox$ starz -c -s 15MB ./brol
brol.00.tar.gz:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar.gz:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar.gz:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```
