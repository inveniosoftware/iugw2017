# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""A custom Invenio data module"""

from setuptools import find_packages, setup

packages = find_packages()

setup(
    name='custom-data-module',
    version=0.1,
    packages=packages,
    include_package_data=True,
    entry_points={
        'invenio_jsonschemas.schemas': [
            'record_jsonschemas = custom_data_module.jsonschemas',
        ],
        'invenio_search.mappings': [
            'custom_record = custom_data_module.mappings',
        ],
        'flask.commands': [
            'custom_demo = custom_data_module.cli:custom_demo',
        ],
        'invenio_records.jsonresolver': [
            'all_records = custom_data_module.jsonresolver',
        ],
        'invenio_pidstore.fetchers': [
            'custid'
            '= custom_data_module.fetchers:custom_record_fetcher',
        ],
        'invenio_pidstore.minters': [
            'custid'
            '= custom_data_module.minters:custom_record_minter',
        ],
    },
    install_requires=[],
)
