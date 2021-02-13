#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:56:40 2020
@author: hoeren
This script will repack the given .tar.gz or .tgz file in chunks no bigger
than denoted by the 
"""
import argparse
import os
import sys
import tarfile
import gzip

import filetype
from tqdm import tqdm

from . import __version__

def is_tar_file(FileName):
    """This function returns true if the supplied FileName holds the magic number for a .tar file."""
    if not os.path.isfile(FileName):
        return False
    kind = filetype.guess(FileName)
    if kind is not None and kind.extension == 'tar':
        return True
    return False

def is_gz_file(FileName):
    """This function returns true if the supplied FileName holds the magic number for a .gz file."""
    if not os.path.isfile(FileName):
        return False
    kind = filetype.guess(FileName)
    if kind is not None and kind.extension == 'gz':
        return True
    return False

def is_tar_gz_file(FileName):
    """This function returns true if the supplied FileName holds the magic number for .gz file, AND 
    the uncompressed contents holds the magic number for a .tar file."""
    if is_gz_file(FileName):
        with gzip.open(FileName, 'rb') as fp:
            contents = fp.read(1024)
        kind = filetype.guess(contents)
        if kind is not None and kind.extension == 'tar':
            return True
    return False

def pack_size(size_str):
    """This function returns the pack size in bytes from a given string.
       A negative number will be returned on fail.
    """
    if len(size_str)<3:
        return -1
    multiplier = size_str[-2:]  # KB, MB or GB
    try:
        size_base = float(size_str[:-2])
    except ValueError:
        return -1
    if multiplier == 'KB':
        size = int(size_base * 1024)
    elif multiplier == 'MB':
        size = int(size_base * 1024 * 1024)
    elif multiplier == 'GB':
        size = int(size_base * 1024 * 1024 * 1024)
    else:
        return -1
    return size

def pack(args):
    """This function packs 'args.SOURCE' (which is guaranteed to be a) directory
       in chunks no bigger than args.size bytes to a .tar file (or a .tar.gz
       file if args.compress is True) The resulting file(s) are generated in
       the args.DESTINATION directory. The resulting file(s) are named after
       the last part of args.SOURCE.
    """
    source_base, source_name = os.path.split(args.SOURCE)
    chunk_sequence = 0
    chunk_size = 0
    destination_base = os.path.join(args.DESTINATION, source_name)
    if args.compress:
        archive_name = f'{destination_base}.{chunk_sequence:02d}.tar.gz'
        destination = tarfile.open(archive_name, 'w|gz')
    else:
        archive_name = f'{destination_base}.{chunk_sequence:02d}.tar'
        destination = tarfile.open(archive_name, 'w')
    if not args.quiet:
        pbar = tqdm(total=args.size, 
                    desc=f"{os.path.basename(archive_name)}",
                    leave=True,
                    ascii=False,
                    unit='Bytes')
        
    for Root, Dirs, Files in os.walk(args.SOURCE):
        for File in Files:
            file_to_add = os.path.join(Root, File)
            file_to_store = file_to_add.replace(source_base, '')[1:]  # cut also the starting '/'
            file_to_add_size = os.path.getsize(file_to_add)
            if chunk_size + file_to_add_size > args.size:
                destination.close()
                chunk_sequence += 1
                chunk_size = 0
                
                if args.compress:
                    archive_name = f'{destination_base}.{chunk_sequence:02d}.tar.gz'
                    destination = tarfile.open(archive_name, 'w|gz')
                else:
                    archive_name = f'{destination_base}.{chunk_sequence:02d}.tar'
                    destination = tarfile.open(archive_name, 'w')

                if not args.quiet:
                    pbar.close()
                    pbar = tqdm(total=args.size, 
                                desc=f"{os.path.basename(archive_name)}",
                                leave=True,
                                ascii=False,
                                unit='Bytes')
            chunk_size += file_to_add_size
            destination.add(file_to_add, arcname=file_to_store)
            if not args.quiet:
                pbar.update(file_to_add_size)
    if not args.quiet:
        pbar.close()
    destination.close()

def repack(args):
    """This function re-packs 'args.SOURCE' (which is guaranteed to be a) .tar
       or .tag.gz file in chunks no bigger than args.size bytes to a .tar file 
       (or a .tar.gz file if args.compress is True) The resulting file(s) are 
       generated in the args.DESTINATION directory. The resulting file(s) are 
       named after the last part of args.SOURCE (minus the .tar or .tar.gz part)
    """
    source_base, source_name = os.path.split(args.SOURCE)
    if is_tar_file(args.SOURCE):
        source = tarfile.open(args.SOURCE, "r")
        if source_name.endswith('.tar'):
            source_name = source_name.replace('.tar', '')
    elif is_tar_gz_file(args.SOURCE):
        source = tarfile.open(args.SOURCE, "r:gz")
        if source_name.endswith('.tar.gz'):
            source_name = source_name.replace('.tar.gz', '')
        if source_name.endswith('.tgz'):
            source_name = source_name.replace('.tgz', '')
    else:
        raise Exception("shouldn't be able to reach this point")
    chunk_sequence = 0
    chunk_size = 0
    destination_base = os.path.join(args.DESTINATION, source_name)

    if args.compress:
        archive_name = f'{destination_base}.{chunk_sequence:02d}.tar.gz'
        destination = tarfile.open(archive_name, 'w|gz')
    else:
        archive_name = f'{destination_base}.{chunk_sequence:02d}.tar'
        destination = tarfile.open(archive_name, 'w')

    if not args.quiet:
        pbar = tqdm(total=args.size, 
                    desc=f"{os.path.basename(archive_name)}",
                    leave=True,
                    ascii=False,
                    unit=' Bytes')

    catalog = source.getmembers()

    for item in catalog:
        if item.isreg:
            file_to_repack = source.extractfile(item)

        if item.size + chunk_size > args.size:
            destination.close()
            chunk_sequence += 1
            chunk_size = 0

            if args.compress:
                archive_name = f'{destination_base}.{chunk_sequence:02d}.tar.gz'
                destination = tarfile.open(archive_name, 'w|gz')
            else:
                archive_name = f'{destination_base}.{chunk_sequence:02d}.tar'
                destination = tarfile.open(archive_name, 'w')
            
            if not args.quiet:
                pbar.close()
                pbar = tqdm(total=args.size, 
                            desc=f"{os.path.basename(archive_name)}",
                            leave=True,
                            ascii=False,
                            unit=' Bytes')
 
        if item.isreg:
            chunk_size += item.size
            destination.addfile(item, file_to_repack)
        else:
            destination.addfile(item)
            
        if not args.quiet:
            pbar.update(item.size)
    if not args.quiet:
        pbar.close()
    destination.close()

def starz(args):
    size = pack_size(args.size)
    if size < 0:
        print(f"Can not interprete '{args.size}'")
        sys.exit(2)
    args.size = size

    if args.version:
        print(f"starz Version {__version__}")
        sys.exit(0)

    if args.DESTINATION.startswith('~'):
        args.DESTINATION = os.path.expanduser(args.DESTINATION)
    args.DESTINATION = os.path.abspath(os.path.realpath(args.DESTINATION))
    if os.path.exists(args.DESTINATION):
        if not os.path.isdir(args.DESTINATION):
            print(f"DESTINATION '{args.DESTINATION}' is to be a directory!")
            sys.exit(3)
    else:
        os.makedirs(args.DESTINATION, exist_ok=True)

    if args.SOURCE.startswith('~'):
        args.SOURCE = os.path.expanduser(args.SOURCE)
    args.SOURCE = os.path.abspath(os.path.realpath(args.SOURCE))
    if not os.path.exists(args.SOURCE):
        print(f"SOURCE '{args.SOURCE}' does not exist.")
        sys.exit(4)
    elif os.path.isdir(args.SOURCE):
        pack(args)
    elif is_tar_file(args.SOURCE) or is_tar_gz_file(args.SOURCE):
        repack(args)
    else:
        print(f"SOURCE '{args.SOURCE}' is not a directory, neither a .tar nor .tar.gz file.")
        sys.exit(5)


def main():
    parser = argparse.ArgumentParser(description='Pack a directory or re-pack a .tag(.gz) file in smaller .tar(.gz) chunks.')

    parser.add_argument('-s', '--size',
                        required=True,
                        help='maximum size (eg. 5GB or 3.14MB)')

    parser.add_argument('-c', '--compress',
                        action='store_true',
                        default=False,
                        help="compress (gzip) the resulting .tar files into .tar.gz")
    
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        default=False,
                        help='surpress the progress bar')

    parser.add_argument('-v', '--version',
                        action='store_true',
                        default=False,
                        help="print the version number")

    parser.add_argument('SOURCE',
                        help='path to either a .tar(.gz) file or a directory')

    parser.add_argument('DESTINATION',
                        nargs='?',
                        default=os.getcwd(),
                        help='destination directory (default is current working directory)')
    
    args = parser.parse_args()
    starz(args)

if __name__ == "__main__":
    main()
