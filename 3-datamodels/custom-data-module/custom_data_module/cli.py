# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 CERN.
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

"""CLI commands for this custom data module."""

from __future__ import absolute_import, print_function

import json
import os
import uuid

import click
import pkg_resources
from flask import url_for
from dojson.contrib.marc21 import marc21, marc21_authority
from dojson.contrib.marc21.utils import create_record, load, split_stream
from flask.cli import with_appcontext
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records.api import Record
from six.moves.urllib.parse import urlunsplit
from invenio_records_rest.utils import allow_all


def import_record(pid, data):
    """Helper enabling to import one record."""
    from invenio_pidstore import current_pidstore
    id_ = uuid.uuid4()
    # Mint a custom Persistent Identifier
    pid = current_pidstore.minters['custid'](id_, data, pid_value=pid)
    # Store record.
    record = Record.create(data, id_=id_)
    click.echo('Created record {}'.format(pid.pid_value))
    return (id_, pid)


def import_records():
    """Helper importing a set of demo records into the database."""
    from flask import current_app
    host = current_app.config.get('JSONSCHEMAS_HOST')
    schema = current_app.extensions['invenio-jsonschemas'].path_to_url(
        'custom_record/custom-record-v1.0.0.json')
    ids = []
    id_, pid = import_record(
        'custom_pid_1',
        {
            "$schema": schema,
            "title": "first custom record",
            "description": "this is a description",
        }
    )
    ids.append(id_)
    id_, _ = import_record(
        'custom_pid_2',
        {
            "$schema": schema,
            "title": "second custom record",
            "description": "this document references the first document",
            "references": [{
                "$ref": 'http://{0}/api/custom_records/{1}#/title'.format(
                    host, pid.pid_value
                )
            }]
        }
    )
    ids.append(id_)
    return ids


@click.group()
def custom_demo():
    """Custom commands."""


@custom_demo.command('init')
@with_appcontext
def load_custom_records():
    """Initialize demo site."""
    from flask import current_app
    current_app.config['RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY'] = \
        allow_all
    # Import bibliographic records
    click.secho('Importing custom records', fg='green')
    records = import_records()
    db.session.commit()
    # Index all records
    click.secho('Indexing records', fg='green')
    indexer = RecordIndexer()
    indexer.bulk_index(records)
    indexer.process_bulk_queue()
