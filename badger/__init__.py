"""
Code for generating different types of repo badges in SVG form.
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import sys
import argparse
import pkg_resources

__version__ = '0.0.2'

DEFAULT_VALUE_COLOR = '#a4a61d'
DEFAULT_LABEL_COLOR = '#555'

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

    def __init__(self, label, value, value_color=DEFAULT_VALUE_COLOR, label_color=DEFAULT_LABEL_COLOR):
        self.label = label
        self.value = value
        self.label_color = label_color
        self.value_color = value_color

    def render(self):
        """
        Read the SVG template from the package, update total, return SVG as a
        string.
        """
        args = {            
            'value': str(self.value),
            'label': self.label,
            'label_width': 10 + 5 * len(self.label),
            'label_color': self.label_color,
            'value_color': self.value_color,
            'value_width': 10 + 5 * len(str(self.value)),
        }

        args['width'] = args['label_width'] + args['value_width']
        args['value_x'] = args['label_width'] + (args['value_width'] / 2)
        args['label_x'] = str(int(args['label_width'] / 2))

        template_path = os.path.join('templates', 'flat.svg')
        template = pkg_resources.resource_string(__name__, template_path).decode('utf8')

        return template.format(**args)


    def save(self, filepath):
        """
        Save badge to the specified path.
        """
        # Write file
        with open(filepath, 'w') as _file:
            _file.write(self.render())

        return filepath

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
        self.color = self.get_color(float(numeric_value))
        

    def get_color(self, total):
        """
        Return color for total relative to minimum and maximum of range.
        """
        xtotal = int(total)

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
