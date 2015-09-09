import dsatutil
import os

def parseArguments():
    """
    Parses arguments
    """
    parser = dsatutil.ArgumentParser(
        description='Outputs information about modified files in SVN without any typical junk that svn status produces'
    )
    parser.add_argument('action', action='store', metavar='svnmod', nargs=1, help='Action name')
    parser.add_argument('directory', action='store', default='.', nargs='?', help='Optional directory name (defaults to .)')
    return parser.parse_args()

def run():
    arguments = parseArguments()
    os.system('/usr/bin/env svn status ' + arguments.directory + ' | /usr/bin/env grep [MADC\\?]');
