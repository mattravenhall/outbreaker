#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup, find_packages

with open("README.md", 'r') as readme:
    long_description = readme.read()

setup(
    name='outbreaker',
    version='1.0.1',
    description='Explore WHO Disease Outbreak News',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matt Ravenhall',
    author_email='matt.ravenhall@gmail.com',
    url='https://github.com/mattravenhall/outbreaker',
    package_dir={"outbreaker": "src"},
    packages=['outbreaker'],
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
