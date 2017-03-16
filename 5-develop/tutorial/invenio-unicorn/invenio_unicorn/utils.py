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

"""Utils module."""

from __future__ import absolute_import, print_function

import uuid

from flask import current_app
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore import current_pidstore
from invenio_records.api import Record


def create_record(data):
    """Create a record.

    :param dict data: The record data.
    """
    indexer = RecordIndexer()
    with db.session.begin_nested():
        # create uuid
        rec_uuid = uuid.uuid4()
        # add the schema
        host = current_app.config.get('JSONSCHEMAS_HOST')
        data["$schema"] = \
            current_app.extensions['invenio-jsonschemas'].path_to_url(
            'custom_record/custom-record-v1.0.0.json')
        # create PID
        current_pidstore.minters['custid'](
          rec_uuid, data, pid_value='custom_pid_{}'.format(rec_uuid)
        )
        # create record
        created_record = Record.create(data, id_=rec_uuid)
        # index the record
        indexer.index(created_record)
    db.session.commit()
