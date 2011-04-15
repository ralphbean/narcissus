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
            "tw2.polymaps",
            "geojson",
        ],
        entry_points={
            'moksha.stream': (
                'narcissus = moksha.apps.narcissus.streams:NarcissusStream',
            ),
            'moksha.consumer': (
                'narcissus = moksha.apps.narcissus.consumers:NarcissusConsumer'
            ),
            'moksha.widget': (
                'narcissus = moksha.widgets.narcissus.widgets:NarcissusWidget',
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
