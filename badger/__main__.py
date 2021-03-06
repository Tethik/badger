"""
Console script to generate SVG badge from a commandline.
"""

import argparse
import logging
import badger


def parse_args(argv=None):
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key')
    parser.add_argument('value')

    parser.add_argument('-o', dest='filepath',
                        help='Save the file to the specified path.')

    parser.add_argument('-p', dest='percentage_mode', action='store_true',
                        help='Percentage mode. Standard green badge.')
    parser.add_argument('-c', dest='color',
                        help='Sets the color of the badge. Must be in hex, e.g. #a4a61d')

    parser.add_argument('-q', dest='quiet', action='store_true',
                        help='Don\'t output any non-error messages.')
    parser.add_argument('-v', dest='print_version', action='version',
                        help='Show version.', version='%(prog)s {}'.format(badger.__version__))
    parser.add_argument('-d', dest='debug', action='store_true')

    # If arguments have been passed in, use them.
    if argv:
        return parser.parse_args(argv)

    # Otherwise, just use sys.argv directly.
    return parser.parse_args()


def main(argv=None):
    """
    Console scripts entry point.
    """
    args = parse_args(argv)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Attempt to parse % type badge automatically.
    if args.percentage_mode:
        badge = badger.PercentageBadge(args.key, float(args.value.replace('%', '')))
    else:
        color = args.color or badger.DEFAULT_VALUE_COLOR
        badge = badger.Badge(args.key, args.value, value_color=color)

    # Show or save output
    if args.filepath:
        path = badge.save(args.filepath)
        if not args.quiet:
            print('Saved badge to "{}"'.format(path))
    else:
        print(badge)

if __name__ == '__main__':
    main()
