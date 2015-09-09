#!/usr/bin/env python

#
# This script is a part of 'dsat' project by Dmitry Dulepov.
#
# @see https://github.com/dmitryd/dsat/
#

import dsatutil
import filecmp
import os
import time

def commonPart(string1, string2):
    """
    Returns the longest common substring from the beginning of sa and sb
     """
    def iter():
        for a, b in zip(string1, string2):
            if a == b:
                yield a
            else:
                return

    return ''.join(iter())


def doStripCommonPaths(abs1, abs2):
    """
    Strips common paths from two file names
    """
    commonDir = commonPart(abs1, abs2)
    if len(commonDir) > 0:
        abs1 = abs1[len(commonDir):]
        abs2 = abs2[len(commonDir):]
    return (abs1, abs2)


def diff(stripCommonPaths, basePath, path1, path2):
    """
    Recursive diff for directories.

    Based on http://atlantic-canary.net/es/rtfm-or-just-code-recursively-compare-directories-and-files-in-two-paths
    """
    # STEP 1: iterate on all path1 paths (directories and filenames) and compare with path2
    # - report if path2 does not exist
    # - when path is a file, report if path1 differ from path2
    common_paths = []
    dateFormat = '%d.%m.%Y %H:%M'
    for path in os.listdir(path1):
        abs1 = os.path.join(path1, path)
        abs2 = os.path.join(path2, path)
        relative = abs1[len(basePath)+1:]
        if not os.path.exists(abs2):
            if stripCommonPaths:
                abs1, abs2 = doStripCommonPaths(abs1, abs2)
            print "[-] %s" % abs1
            continue
        common_paths.append(relative)

        if os.path.isfile(abs1):
            r = filecmp.cmp(abs1, abs2)
            if not r:
                mtime1 = os.path.getmtime(abs1)
                mtime2 = os.path.getmtime(abs2)
                time1 = time.strftime(dateFormat, time.localtime(mtime1))
                time2 = time.strftime(dateFormat, time.localtime(mtime2))
                if stripCommonPaths:
                    abs1, abs2 = doStripCommonPaths(abs1, abs2)
                if mtime1 > mtime2:
                    print "[N] %s (%s) vs %s (%s)" % (abs1, time1, abs2, time2)
                else:
                    print "[O] %s (%s) vs %s (%s)" % (abs1, time1, abs2, time2)
        elif os.path.isdir(abs1):
            paths = diff(stripCommonPaths, basePath, abs1, abs2)
            common_paths.extend(paths)

    # STEP 2: the other way: iterate on all path2 paths and
    # - report if path in path2 does not exist in path1
    for path in os.listdir(path2):
        abs1 = os.path.join(path1, path)
        abs2 = os.path.join(path2, path)
        if not os.path.exists(abs1):
            if stripCommonPaths:
                abs1, abs2 = doStripCommonPaths(abs1, abs2)
            print "[+] %s" % abs2

    return common_paths


def parseArguments():
    """
    Parses arguments
    """
    parser = dsatutil.ArgumentParser(
        description='Compares directories recursively and outputs file differences',
        epilog='M|Result is a list of files prefixed as follows:\n' +
            '  [N] File in dir2 (or in dir1 if -r) is newer than the file in the other directory\n' +
            '  [+] File only exists in dir2 (or dir1 if -r)\n' +
            '  [-] File only exists in dir1 (or dir2 if -r)\n' +
            'Time stamps are in the european format and shown only for different files.'
    )
    parser.add_argument('action', action='store', metavar='dirdiff', nargs=1, help='Action name')
    parser.add_argument('dir1', action='store', nargs=1, help='First directory')
    parser.add_argument('dir2', action='store', nargs=1, help='Second directory')
    parser.add_argument('--full-paths', action='store_true', default=False, required=False, help='Do not strip common paths in results')
    #parser.add_argument('-q', action='store_true', default=False, required=False, help='Do not show differences in files, just say they are different')
    parser.add_argument('-r', action='store_true', default=True, required=False, help='Reverse order of comparison')
    #parser.add_argument('-w', action='store_true', default=True, required=False, help='Ignore all whitespace (set by default, slower!)')
    arguments = parser.parse_args()
    return arguments


def run():
    """
    Runs the action
    """
    arguments = parseArguments()
    if arguments.r:
        paths = [arguments.dir2[0], arguments.dir1[0]]
    else:
        paths = [arguments.dir1[0], arguments.dir2[0]]
    for path in paths:
        if not os.path.exists(path):
            print "%s does not exist!" % path
            exit()

    basepath = os.path.commonprefix(paths).rstrip('/')
    diff(not arguments.full_paths, basepath, *paths)
