#!/usr/bin/env python

#
# This script is a part of 'dsat' project by Dmitry Dulepov.
#
# @see https://github.com/dmitryd/dsat/
#
# Based on http://atlantic-canary.net/es/rtfm-or-just-code-recursively-compare-directories-and-files-in-two-paths

import argparse
import filecmp
import os
import os.path
import sys

def diff(basepath, path1, path2):
    # STEP 1: iterate on all path1 paths (directories and filenames) and compare with path2
    # - report if path2 does not exist
    # - when path is a file, report if path1 differ from path2
    common_paths = []
    for path in os.listdir(path1):
        abs1 = os.path.join(path1, path)
        abs2 = os.path.join(path2, path)
        relative = abs1[len(basepath)+1:]
        if not os.path.exists(abs2):
            print "Only in %s: %s" % (os.path.dirname(abs1), path)
            continue
        common_paths.append(relative)

        if os.path.isfile(abs1):
            r = filecmp.cmp(abs1, abs2)
            if not r:
                print "Files %s and %s differ" % (abs1, abs2)
        elif os.path.isdir(abs1):
            paths = diff(basepath, abs1, abs2)
            common_paths.extend(paths)

    # STEP 2: the other way: iterate on all path2 paths and
    # - report if path in path2 does not exist in path1
    for path in os.listdir(path2):
        abs1 = os.path.join(path1, path)
        abs2 = os.path.join(path2, path)
        relative = abs2[len(basepath)+1:]
        if not os.path.exists(abs1):
            print "Only in %s: %s" % (os.path.dirname(abs2), path)

    return common_paths


def parseArguments():
    parser = argparse.ArgumentParser(description='System administration tool')
    parser.add_argument('action', action='store', metavar='dirdiff', nargs=1, help='Action name')
    parser.add_argument('dir1', action='store', nargs=1, help='First directory')
    parser.add_argument('dir2', action='store', nargs=1, help='Second directory')
    parser.add_argument('-q', action='store_true', default=True, required=False, help='Do not show differences in files, just say they are different')
    arguments = parser.parse_args()
    return arguments

def run():
    arguments = parseArguments()
    paths = [arguments.dir1[0], arguments.dir2[0]]
    for path in paths:
        if not os.path.exists(path):
            print "%s does not exist!" % path
            exit()

    basepath = os.path.commonprefix(paths).rstrip('/')
    diff(basepath, *paths)
