#
# This script is a part of 'dsat' project by Dmitry Dulepov.
#
# @see https://github.com/dmitryd/dsat/
#

import argparse

class SmartFormatter(argparse.HelpFormatter):
    """
    This class will format text starting from "M|" to multiline.
    """
    def _format_text(self, text):
        """
        Formats text with new lines if necessary
        """
        if text.startswith('M|'):
            return text[2:]
        return argparse.HelpFormatter._format_text(self, text)


class ArgumentParser(argparse.ArgumentParser):
    """
    Defines an argument parser with our formatter and description.
    """
    def __init__(self,
            prog=None,
            usage=None,
            description='dsat - system administration tool',
            epilog=None,
            version=None,
            parents=[],
            formatter_class=SmartFormatter,
            prefix_chars='-',
            fromfile_prefix_chars=None,
            argument_default=None,
            conflict_handler='error',
            add_help=True):
        argparse.ArgumentParser.__init__(self,
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            version=version,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help)
