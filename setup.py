from setuptools import setup, find_packages

VERSION = "0.0.3"
with open("LICENSE") as f:
    LICENSE = f.read()
with open("README.md") as f:
    README = f.read()

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
