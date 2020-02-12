#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='outbreaker',
    version='1.0',
    description='Explore WHO Disease Outbreak News',
    author='MattR',
    url='https://github.com/mattravenhall/outbreaker',
    package_dir={"outbreaker": "src"},
    packages=['outbreaker'],
    # include_package_data=True,
    # exclude_package_data={"": ["README.txt"]},
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
    entry_points={
        "console_scripts": [
            'outbreaker=outbreaker.__main__:main'
        ]
    },
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'pandas>=0.19.2',
        'requests'
    ],
    python_requires='>=3.7',
)