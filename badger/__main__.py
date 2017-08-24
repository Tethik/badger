"""
Generate coverage badges for Coverage.py.
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import sys
import argparse
import pkg_resources

__version__ = '0.0.1'


DEFAULT_COLOR = '#a4a61d'
COLORS = {
    'brightgreen': '#4c1',
    'green': '#97CA00',
    'yellowgreen': '#a4a61d',
    'yellow': '#dfb317',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'lightgrey': '#9f9f9f',
}

COLOR_RANGES = [
    (95, 'brightgreen'),
    (90, 'green'),
    (75, 'yellowgreen'),
    (60, 'yellow'),
    (40, 'orange'),
    (0, 'red'),
]

def get_color(total):
    """
    Return color for current coverage precent
    """
    try:
        xtotal = int(total)
    except ValueError:
        return COLORS['lightgrey']
    for range_, color in COLOR_RANGES:
        if xtotal >= range_:
            return COLORS[color]


def get_badge(key, value, color=DEFAULT_COLOR):
    """
    Read the SVG template from the package, update total, return SVG as a
    string.
    """
    key_width = max(80, 10 + 9 * len(key))
    value_width = max(36, 10 + 9 * len(value))
    print(key_width)
    print(value_width)
    width = max(99, key_width + value_width)
    value_x = key_width + (value_width / 2)
    template_path = os.path.join('templates', 'flat.svg')
    template = pkg_resources.resource_string(__name__, template_path).decode('utf8')
    return template\
      .replace('{{ key }}', key)\
      .replace('{{ color }}', color)\
      .replace('{{ value }}', value)\
      .replace('{{ width }}', str(width))\
      .replace('{{ value_x }}', str(value_x))\
      .replace('{{ key_width }}', str(key_width))\
      .replace('{{ key_x }}', str(int(key_width / 2)))\
      .replace('{{ value_width }}', str(value_width))


def parse_args(argv=None):
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('value')

    # parser.add_argument('--max', dest='max',
    #                     help='Max value')
    # parser.add_argument('--min', dest='min',
    #                     help='Min value')

    parser.add_argument('-o', dest='filepath',
                        help='Save the file to the specified path.')
    parser.add_argument('-p', dest='plain_color', action='store_true',
                        help='Plain color mode. Standard green badge.')
    parser.add_argument('-f', dest='force', action='store_true',
                        help='Force overwrite image, use with -o key.')
    parser.add_argument('-q', dest='quiet', action='store_true',
                        help='Don\'t output any non-error messages.')
    parser.add_argument('-v', dest='print_version', action='store_true',
                        help='Show version.')

    # If arguments have been passed in, use them.
    if argv:
        return parser.parse_args(argv)

    # Otherwise, just use sys.argv directly.
    return parser.parse_args()


def save_badge(badge, filepath, force=False):
    """
    Save badge to the specified path.
    """
    # Validate path (part 1)
    if filepath.endswith('/'):
        print('Error: Filepath may not be a directory.')
        sys.exit(1)

    # Get absolute filepath
    path = os.path.abspath(filepath)
    if not path.lower().endswith('.svg'):
        path += '.svg'

    # Validate path (part 2)
    if not force and os.path.exists(path):
        print('Error: "{}" already exists.'.format(path))
        sys.exit(1)

    # Write file
    with open(path, 'w') as _file:
        _file.write(badge)

    return path


def main(argv=None):
    """
    Console scripts entry point.
    """
    args = parse_args(argv)

    # Print version
    if args.print_version:
        print('badger v{}'.format(__version__))
        sys.exit(0)


    percentage = args.value
    color = DEFAULT_COLOR if args.plain_color else get_color(percentage)
    badge = get_badge(args.key, args.value, color)


    # Show or save output
    if args.filepath:
        path = save_badge(badge, args.filepath, args.force)
        if not args.quiet:
            print('Saved badge to {}'.format(path))
    else:
        print(badge, end='')


if __name__ == '__main__':
    main()
