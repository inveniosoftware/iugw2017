..
    This file is part of Invenio.
    Copyright (C) 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

====================
 Custom-Data-Module
====================

The goal of this module is to show the different aspect of Invenio's datamodel.

Install
-------

First go in the virtual machine:

.. code-block:: console

    laptop> vagrant ssh web
    vagrant> source .inveniorc
    vagrant> workon invenio

First install the module.

.. code-block:: console

    vagrant> cd /vagrant/3-datamodels/custom-data-module/
    vagrant> pip install .


Then update your instance configuration.

.. code-block:: console

    vagrant> cat invenio.cfg >> ~/.virtualenvs/invenio/var/instance/invenio.cfg


Then recreate the search indices:

.. code-block:: console

    vagrant> invenio index destroy --force --yes-i-know
    vagrant> invenio index init
    vagrant> invenio index reindex --yes-i-know
    vagrant> invenio index run


Initialize the module, this will create a few demonstration records:

.. code-block:: console

    vagrant> invenio custom_demo init


Then start Invenio.

.. code-block:: console

    vagrant> invenio run -h 0.0.0.0


Our new records should be accessible at

http://192.168.50.10/custom_records/custom_pid_1

http://192.168.50.10/custom_records/custom_pid_2

and via the REST API at

http://192.168.50.10/api/custom_records/custom_pid_1

http://192.168.50.10/api/custom_records/custom_pid_2


Tutorial:
---------

1. Invenio documentation
^^^^^^^^^^^^^^^^^^^^^^^^

Read `Invenio documentation about data models
<http://invenio.readthedocs.io/en/feature-ils/developersguide/create-a-datamodel.html>`_
which explains how Invenio stores records.


2. See a simple record in the UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go see the first record with your browser:

http://192.168.50.10/custom_records/custom_pid_1

This is a simple record. It contains the following fields:
* "title" and "description": some custom fields we added to our document.
* "custom_pid": contains a reference to our custom Persistent Identifier.
* "$schema": a **reference to the JSON Schema** which validates this record.

Go to the '$schema' url. You can now see the JSON schema.


3. JSON Schemas
^^^^^^^^^^^^^^^

The **JSON Schema** which is referenced by the record can be found here:

**custom_data_module/jsonschemas/custom_record/custom-record-v1.0.0.json**

Invenio can serve the JSON schemas itself, but it can also use external
JSON Schemas as long as an URI is available.


4. Persistent Identifiers
^^^^^^^^^^^^^^^^^^^^^^^^^

Go to:

http://192.168.50.10/records/1

This records uses a numeric persistent identifier "1". It can be seen under
*contro_number*. It is also present in the URI of the record.

See how the URI is different from our custom record. Invenio gives access
to records via their persistent identifier. Multiple **Persistent Identifier
types** can be attached to a record but not all of them need to be exposed
as URIs.

Example: B2SHARE uses both EPIC PID and DOI.

This means that you can have one URL for each type of record

Example: http://192.168.50.10/authors/<ORCID>


5. REST API
^^^^^^^^^^^

Go to:

http://192.168.50.10/api/custom_records/custom_pid_1

This is the REST API endpoint for our custom record "custom_pid_1". It returns
it in the JSON format.

The REST API also enables different URIs for different Persistent Identifier
types. Go see:

http://192.168.50.10/api/records/1

The REST API not only enables to read records but also to create new ones
and to modify existing ones.


6. Serialization
^^^^^^^^^^^^^^^^

Compare:

http://192.168.50.10/custom_records/custom_pid_1

and

http://192.168.50.10/api/custom_records/custom_pid_1

You might have noticed that the record returned by the REST API has some
additional information we didn't see in the User Interface. It has
some links.

Invenio enables to change the way a record is exposed to the outside world.
For the REST API this is done via **serializers**. This enables us to export
records in any format we want: MARC 21, JSON, Dublin Core...

Run the following command on your laptop:
.. code-block:: console

    laptop> curl -XGET 'http://192.168.50.10/api/custom_records/custom_pid_1'

Here you can see the same result as the one given by the browser.

Now we will ask the same record but instead of requiring a JSON output we
will ask for a plain text result.
Run the following command on your laptop:
.. code-block:: console

    laptop> curl  -H "Accept:text/plain" -XGET 'http://192.168.50.10/api/custom_records/custom_pid_1'

The result just shows the title as plain text. The serializer which creates
this result is here:

custom_data_module/serializers.py

The function *plain_text_serializer* just takes the title and returns it.


7. Search
^^^^^^^^^

Go to:

http://192.168.50.10/api/custom_records/

We just did a search request. The *hits* array contain a list of found records.
As we didn't filter the query, this shows the two records we created at the
beginning.

Now we will ask for records matching the query "references". Go to:

http://192.168.50.10/api/custom_records/?q=references

This filters the searched record with the query "references". Only the
second record is returned as its description contains the word "references".

Now we will ask for records matching the query "abcd". Go to:

http://192.168.50.10/api/custom_records/?q=abcd

No record is retured as the word "abcd" is not present in any of the records.

Now we will ask for records matching the query "refer". Go to:

http://192.168.50.10/api/custom_records/?q=refer

The second record is still return even though it does not contain the word
"refer". This is possible because we asked our search engine to analyze the
text as "english".

Open the file:

**custom_data_module/mappings/custom_record/custom-record-v1.0.0.json**

This is the Elasticearch Mapping which enables to tell our search engine
how to analyze the text. You can go see Elasticsearch documentation
for more information about mappings files.

This is also why we had to recreate the search indices at the beginning of
this tutorial. We had just added this new mapping file when we installed
the module.


8. Resolving references
^^^^^^^^^^^^^^^^^^^^^^^

Compare:

http://192.168.50.10/custom_records/custom_pid_2

and

http://192.168.50.10/api/custom_records/custom_pid_2

The User Interface shows a "$ref" field which is instead resolved as
the first document's title. The "$ref" is a JSON Reference to the first
document's title. Our JSON serializer resolves the reference and replaces
it with the title.

Note that if document "custom_pid_1" changed we would need to reindex
document "custom_pid_2" or the search would still have the previously
referenced value.
