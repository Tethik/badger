import re
import sys
from setuptools import setup, find_packages

with open('badger/version.py', 'r') as fd:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
with open("LICENSE") as f:
    LICENSE = f.read()
with open("README.rst") as f:
    README = f.read()

if len(sys.argv) > 1 and sys.argv[1] == "bdist_wheel":
    # Lets update the readme with build info before releasing ;)
    import pytest
    import badger
    
    pytest.main(['--cov=badger', '--cov-report=xml', '--junit-xml=test-results.xml'])
    print()
    with open('coverage.xml') as cover_file:
        contents = cover_file.read()
        coverage = float(re.search(r'line-rate="(\d.?\d*)"', contents, re.MULTILINE).group(1))
        print(coverage)

    badger.PercentageBadge("coverage", round(100 * coverage, 2)).save('examples/coverage.svg')
    badger.Badge("version", VERSION).save('examples/version.svg')

    with open('README.rst', 'w') as f:
        README = re.sub(r'v\d.\d.\d', 'v'+VERSION, README)
        README = re.sub(r'\d+\.?\d*%', '{:.2%}'.format(coverage), README)
        README = re.sub(r'\("coverage", \d+\.?\d*\)', '("coverage", {0:.2f})'.format(100 * coverage), README)        
        f.write(README)


setup(
    name='badger',
    version=VERSION,
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Commandline Interface to create shields.io style badges as SVG.',
    long_description=README,
    url='https://github.com/Tethik/badger',
    packages=['badger'],
    entry_points = {
        'console_scripts': ['badger=badger.__main__:main'],
    },
    zip_safe=True,
    include_package_data=True,
    install_requires=[
        'freetype-py',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    license=LICENSE,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
    ]
)
