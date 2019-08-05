#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='python_modeler',
    version='0.1.0',
    description='3D modeling in Python.',
    author='Todd Young',
    author_email='youngmt1@ornl.gov',
    url='https://github.com/yngtodd/modeler',
    packages=[
        'modeler',
    ],
    package_dir={'modeler': 'modeler'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='modeler',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
