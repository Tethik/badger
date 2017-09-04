import math
import sys
import re
import badger


report_file, svg_file = sys.argv[1], sys.argv[2]

regex = re.compile(r'branch-rate="(\d+\.\d+)%?"', re.MULTILINE)

text = open(report_file).read()

match = re.search(regex, text)
total_line_precent = float(match.group(1)) * 100
print(total_line_precent)
badge = badger.PercentageBadge('coverage', total_line_precent)
badge.save(svg_file)
