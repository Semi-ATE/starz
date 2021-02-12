# starz
**S**ized **T**ape **AR**chive**Z**

This small command line tool creates sized (gzipped) tar files from either a (gzipped) tar or a directory.

The 'raison d'être' of this tool is because [GitHub Packages](https://github.com/features/packages) limits the layer size of a docker container to 5GB.
This poses a problem when one needs to install huge tarballs (eg: [PetaLinux](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-design-tools.html), [vivado](https://www.xilinx.com/support/download.html), ...)

The Unix [split](https://www.man7.org/linux/man-pages/man1/split.1.html) command will **not** do as each resulting 'split' is not individual un-tar-able, and after a [cat](https://www.man7.org/linux/man-pages/man1/cat.1.html) of the individual parts, we violate the 5GB layer constraint again.
 
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Semi-ATE/starz/blob/main/LICENSE)
[![CI](https://github.com/Semi-ATE/starz/workflows/CI/badge.svg)](https://github.com/Semi-ATE/starz/actions?query=workflow%3ACI)

# Installation

## conda (preferred)

```sh
me@mybox$ conda install starz
```

## pip

```sh
me@mybox$ pip install starz
```

# Usage

```sh
me@mybox$ stars --help
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

```sh
me@mybox$ starz -s 15MB brol.tar.gz
brol.00.tar:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```

re-packing a bin gzipped-tar file in smaller gzipped-tar files :

```sh
me@mybox$ starz -c -s 15MB brol.tar.gz
brol.00.tar.gz:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar.gz:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar.gz:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```

same as above, but not outputting progress bar :

```sh
me@mybox$ starz -q -c -s 15MB brol.tar.gz
me@mybox$ 
```

packing the `./brol` directory (recursively) in compressed-tar files with less than 15MB of content each:

```sh
me@mybox$ starz -c -s 15MB ./brol
brol.00.tar.gz:  18%|█████                   | 2808448/15728640 [00:00<00:00, 30900007.82 Bytes/s]
brol.01.tar.gz:  99%|███████████████████████▊| 15633123/15728640 [00:00<00:00, 223312287.21 Bytes/s]
brol.02.tar.gz:  43%|███████████             | 6751263/15728640 [00:00<00:00, 151304825.55 Bytes/s]
me@mybox$ 
```

