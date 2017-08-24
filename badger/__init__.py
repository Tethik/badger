"""
Code for generating different types of repo badges in SVG form.
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


class Badge(object):
    """
    Class that generates the SVG for a single badge in the following format:
        label | value
    label and value can be any string.
    """

    def __init__(self, label, value, color=DEFAULT_COLOR):
        self.label = label
        self.value = value
        self.color = color

    def render(self):
        """
        Read the SVG template from the package, update total, return SVG as a
        string.
        """
        label_width = max(80, 10 + 9 * len(self.label))
        value_width = max(36, 10 + 9 * len(str(self.value)))
        width = max(99, label_width + value_width)
        value_x = label_width + (value_width / 2)
        template_path = os.path.join('templates', 'flat.svg')
        template = pkg_resources.resource_string(__name__, template_path).decode('utf8')

        return template\
            .replace('{{ label }}', self.label)\
            .replace('{{ color }}', self.color)\
            .replace('{{ value }}', str(self.value))\
            .replace('{{ width }}', str(width))\
            .replace('{{ value_x }}', str(value_x))\
            .replace('{{ label_width }}', str(label_width))\
            .replace('{{ label_x }}', str(int(label_width / 2)))\
            .replace('{{ value_width }}', str(value_width))

    def save(self, filepath, force=False):
        """
        Save badge to the specified path.
        """
        # Validate path (part 1)
        if filepath.endswith('/'):
            raise IOError('Error: Filepath may not be a directory.')

        # Get absolute filepath
        path = os.path.abspath(filepath)
        if not path.lower().endswith('.svg'):
            path += '.svg'

        # Validate path (part 2)
        if not force and os.path.exists(path):
            raise FileExistsError('Error: "{}" already exists.'.format(path))

        # Write file
        with open(path, 'w') as _file:
            _file.write(self.render())

        return path

    def __str__(self):
        return self.render()

class ColorRangeBadge(Badge):
    """
    A badge that automatically picks a color between red and green based on a
    numeric value.
    """

    def __init__(self, label, numeric_value, minimum=0, maximum=100):
        super(ColorRangeBadge, self).__init__(label, numeric_value)
        self.minimum = minimum
        self.maximum = maximum        
        self.color = self.get_color(numeric_value)
        

    def get_color(self, total):
        """
        Return color for total relative to minimum and maximum of range.
        """
        try:
            xtotal = int(total)
        except ValueError:
            return COLORS['lightgrey']

        factor = 100 / (self.maximum - self.minimum)
        print(factor)
        for _range, color in COLOR_RANGES:
            if xtotal >= _range * factor:
                return COLORS[color]

class PercentageBadge(ColorRangeBadge):
    """
    Badge that takes a percentage value between 0-100 and automatically renders with a relative red to green color range.
    """

    def __init__(self, label, numeric_value):
        super(PercentageBadge, self).__init__(label, numeric_value, 0, 100)
        self.value = str(numeric_value) + '%'
