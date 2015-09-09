# About dsat

`dsat` stands for Dmitry's System Administration Tool. It is created to simplify routine tasks that *nix console users do.

The tool is not only meant for system administrators but also for web programmers.

## Usage

### dsat dirdiff

usage: dsat [-h] [--full-paths] [-r] dirdiff dir1 dir2

Compares directories recursively and outputs file differences

positional arguments:  
  dirdiff       Action name
  dir1          First directory
  dir2          Second directory

optional arguments:  
  -h, --help    show this help message and exit
  --full-paths  Do not strip common paths in results
  -r            Reverse order of comparison

Result is a list of files prefixed as follows:

- [N] File in dir2 (or in dir1 if -r) is newer than the file in the other directory
- [+] File only exists in dir2 (or dir1 if -r)
- [-] File only exists in dir1 (or dir2 if -r)

Time stamps are in the european format and shown only for different files.

### dsat gffp
usage: dsat [-h] gffp

Publishes the current feature branch

positional arguments:  
  gffp        Action name

### dsat svnmod

usage: dsat [-h] svnmod [directory]

Outputs information about modified files in SVN without any typical junk that svn status produces

positional arguments:  
  svnmod      Action name
  directory   Optional directory name (defaults to .)



Complete list of options can be found by running either `dsat -h` or `dsat --help` or `dsat help`.

You need to `chmod +x dsat` obviously.

## Planned functions

### File system
- [dirdiff] -w option to ignore all files with only whitespace difference (same as diff -qwB)

### Git
- [gffs] Git flow feature start
- [gffp] Got flow feature publish current feature
- [git cleanup] All kind of automatic clean up for the local and remote repos
