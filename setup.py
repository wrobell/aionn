#!/usr/bin/env python3
#
# aionn - asyncio messaging library based on nanomsg and nnpy
#
# Copyright (C) 2016 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

setup(
    name='aionn',
    version='0.1.0',
    description='aionn - asyncio messaging library based on nanomsg and nnpy',
    author='Artur Wroblewski',
    author_email='wrobell@riseup.net',
    url='http://wrobell.it-zone.org/aionn/',
    setup_requires = ['setuptools_git >= 1.0',],
    packages=find_packages('.'),
    include_package_data=True,
    long_description=\
"""\
Aionn is Python asyncio messaging library based on nanomsg and nnpy.
""",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
    ],
    keywords='asyncio messaging',
    license='GPL',
    install_requires=['nnpy >= 1.3'],
    test_suite='nose.collector',
)

# vim: sw=4:et:ai
