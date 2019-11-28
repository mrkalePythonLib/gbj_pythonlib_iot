#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup function for the package."""

from setuptools import setup

setup(
  name='gbj_pythonlib_iot',
  version='1.0.0',
  description='Python device libraries for IoT support.',
  long_description='Modules suitable for specific handling of devices used'
  'for internet of things in python scripts.',
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Topic :: System :: Hardware',
  ],
  keywords='common, system, fan',
  url='http://github.com/mrkalePythonLib/gbj_pythonlib_iot',
  author='Libor Gabaj',
  author_email='libor.gabaj@gmail.com',
  license='MIT',
  packages=['gbj_pythonlib_iot'],
  install_requires=[],
  include_package_data=True,
  zip_safe=False
)
