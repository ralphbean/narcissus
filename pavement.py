# -*- coding: utf-8 -*-
from paver.easy import *
from paver.setuputils import (setup, find_package_data, find_packages,
                              install_distutils_tasks)
install_distutils_tasks()
from moksha.lib.paver_tasks import *

options(
    setup=Bunch(
        name="narcissus",
        version="0.1",
        release="1",
        url="http://moksha.fedorahosted.org",
        description="Describe your package here",
        license="ASL 2.0",
        long_description="",
        author="",
        author_email="",
        rpm_name='narcissus',
        packages=find_packages(),
        package_data=find_package_data(),
        namespace_packages=[
            'moksha',
            'moksha.apps',
            'moksha.widgets',
        ],
        install_requires=[
            "Moksha",
            "tw2.polymaps>=0.1a3",
            "tw2.jqplugins.jqplot",
            "geojson",
            "pygeoip",
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
                'narc_plot = moksha.widgets.narcissus.widgets:NarcissusPlotWidget',
            ),
            'moksha.connector': (
                'narcissus = moksha.apps.narcissus.connector:NarcissusConnector'
            ),
            'moksha.application': (
                'narcissus = moksha.apps.narcissus.controllers:NarcissusController'
            ),
        }
    ),
)
