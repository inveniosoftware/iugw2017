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

"""Record serialization."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify
from invenio_records_rest.serializers.schemas.json import RecordSchemaJSONV1


json_v1 = JSONSerializer(RecordSchemaJSONV1, replace_refs=True)
"""JSON v1 serializer resolving all $ref fields."""

json_v1_response = record_responsify(json_v1, 'application/json')
"""JSON response builder that uses the JSON v1 serializer."""

json_v1_search = search_responsify(json_v1, 'application/json')
"""JSON search response builder that uses the JSON v1 serializer."""


def plain_text_serializer(pid, record, code=200, headers=None, **kwargs):
    """Example of a custom serializer which just returns the record's title."""
    response = current_app.response_class()

    # the returned data will just contain the title
    response.data = record['title']

    # set the return code in order to notify any error
    response.status_code = code

    # update headers
    response.headers['Content-Type'] = 'text/plain'
    if headers is not None:
        response.headers.extend(headers)
    return response
