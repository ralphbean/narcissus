# This file is part of Narcissus
# Copyright (C) 2011-2013  Ralph Bean
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import sys

f = open('README.rst')
long_description = f.read().strip()
f.close()

setup(
    name='narcissus.app',
    version='0.9.0.1',
    description='WSGI app for Narcissus, realtime log visualization',
    long_description=long_description,
    license="AGPLv3+",
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://narcissus.ws',
    install_requires=[
        "narcissus.common",
        "flask",
        "moksha.wsgi",
        "tw2.polymaps",
        "tw2.jqplugins.jqplot",
        "tw2.slideymenu",
        #"tw2.jit",
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    namespace_packages=['narcissus'],
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': (
            'narcissus.app-serve=narcissus.app.routes:main',
        ),
    },

)
