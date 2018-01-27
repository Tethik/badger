"""
A script to generate different sized badges in a html file for a quick overview.
"""

import badger

# https://stackoverflow.com/a/33043558/3679116
html = """
<!DOCTYPE HTML>
<html>
<head>
<style> 
body, html {{
    width: 100%;
    height: 100%;
}}
</style>
</head>
<body>
<div>
{}
</div>
</body>
"""

def main():
    pairs = [
        ("build", "succeeded"),
        ("build", "failed"),
        ("a label that is longer than usual", "value"),
        ("label", "a value that is longer than usual"),
        ("a label that is longer than usual", "a value that is longer than usual"),
    ]

    badges = []
    i = 0
    for label, value in pairs:
        badge = badger.Badge(label, value)
        # filename = "{i}.svg".format(i=i)
        # badge.save(filename)
        # badges.append("<img src='{filename}'>".format(filename=filename))
        badges.append("<object>" + badge.render() + "</object>")
        i += 1

    print(html.format("<br />\n".join(badges)))

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    main()
