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
    name='narcissus.hub',
    version='0.9.0.1',
    description='Hub components for Narcissus, realtime log visualization',
    long_description=long_description,
    license="AGPLv3+",
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://narcissus.ws/',
    install_requires=[
        "moksha.hub",
        "pygeoip",
        "geojson",
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
        'moksha.stream' : (
            ## Enable this to *test* narcissus.  It produces random ips.
            #'random_lol = narcissus.hub.producers:RandomIPProducer',

            # We used to keep these in an rrd database.  That was too heavy.
            #'series_pro = narcissus.hub.consumers:TimeSeriesProducer',
        ),
        'moksha.consumer': (
            'raw_ip =     narcissus.hub.consumers:RawIPConsumer',
            'httpdlight = narcissus.hub.consumers:HttpLightConsumer',
            'latlon2geo = narcissus.hub.consumers:LatLon2GeoJsonConsumer',

            # We used to keep these in an rrd database.  That was too heavy.
            #'series_con = narcissus.hub.consumers:TimeSeriesConsumer',
        ),
    },
)
