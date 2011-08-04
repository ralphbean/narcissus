# -*- coding: utf-8 -*-
import sys, os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

README = README.split(".. split here")[1]

setup(
    name="narcissus",
    version="0.1.0",
    url="http://moksha.fedorahosted.org",
    description="Realtime visualizations of web server hits",
    license="ASL 2.0",
    long_description=README,
    author="Ralph Bean",
    author_email="ralph.bean@gmail.com",
    rpm_name='narcissus',
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=[
        'moksha',
        'moksha.apps',
        'moksha.widgets',
    ],
    install_requires=[
        "Moksha",
        "sqlalchemy",
        "pymysql_sa",
        "MySQL-python",
        "zope.sqlalchemy",
        "decorator",
        "ansi2html>=0.6.0",
        "geojson",
        "pygeoip",
        "tw2.polymaps>=0.1a3",
        "tw2.jqplugins.jqplot",
        "tw2.slideymenu>=2.0b1",
        "tw2.rrd>=2.0b13",
        "tw2.jit>=0.3.0",
    ],
    entry_points={
        'moksha.root' : (
            'root = moksha.apps.narcissus.controllers.root:NarcissusController',
        ),
        'moksha.stream' : (
            'series_pro = moksha.apps.narcissus.consumers:TimeSeriesProducer',
        ),
        'moksha.consumer': (
            'httpdlight = moksha.apps.narcissus.consumers:HttpLightConsumer',
            'latlon2geo = moksha.apps.narcissus.consumers:LatLon2GeoJsonConsumer',
            'series_con = moksha.apps.narcissus.consumers:TimeSeriesConsumer',
        ),
        'moksha.widget': (
            'narc_map = moksha.widgets.narcissus.widgets:NarcissusMapWidget',
            'narc_graph = moksha.widgets.narcissus.widgets:NarcissusGraphWidget',
            'narc_plot = moksha.widgets.narcissus.widgets:NarcissusPlotWidget',
        ),
        'moksha.connector': (
            'narcissus = moksha.apps.narcissus.connector:NarcissusConnector'
        ),
        'moksha.application': (
            'narcissus = moksha.apps.narcissus.controllers:NarcissusController'
        ),
    }
)
