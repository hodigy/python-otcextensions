#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
import mock
# from osc_lib import utils as common_utils

from otcextensions.osclient.rds.v1 import datastore
from otcextensions.tests.unit.osclient.rds.v1 import fakes as rds_fakes


class TestRdsDatastoreTypes(rds_fakes.TestRds):

    columns_datastore_type = ('Name', )

    def setUp(self):
        super(TestRdsDatastoreTypes, self).setUp()

        self.cmd = datastore.ListTypes(self.app, None)

        self.app.client_manager.rds.datastore_types = mock.Mock()

        self.datastore_types = []
        self.datastore_type_data = []
        for ds in ['MySQL', 'PostgreSQL', 'SQLServer']:
            obj = type('obj', (object,), {'name': ds})
            self.datastore_types.append(obj)
            # Since only one field is there leave a comma at the end
            self.datastore_type_data.append((ds,))

    def test_list_datastore_types(self):
        arglist = [
        ]

        verifylist = [
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.datastore_types.side_effect = [
            self.datastore_types
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.datastore_types.assert_called()

        self.assertEqual(self.columns_datastore_type, columns)
        self.assertEqual(tuple(self.datastore_type_data), tuple(data))


class TestRdsDatastoreVersions(rds_fakes.TestRds):
    column_headers = (
        'ID',
        'Name',
        'Datastore',
        'Image',
        'Packages'
    )

    def setUp(self):
        super(TestRdsDatastoreVersions, self).setUp()

        self.cmd = datastore.ListDatastoreVersions(self.app, None)

        self.app.client_manager.rds.datastores = mock.Mock()

        self.datastores = self.datastore_mock.create_datastores(3)
        self.datastore_data = []

        for s in self.datastores:
            self.datastore_data.append((
                s.id,
                s.name,
                s.datastore,
                s.image,
                s.packages,
            ))

    def test_list_datastore_versions(self):
        arglist = [
            '--type=test_type'
        ]

        verifylist = [
            ('type', 'test_type')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.app.client_manager.rds.datastores.side_effect = [
            self.datastores
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.app.client_manager.rds.datastores.assert_called()

        self.assertEqual(self.column_headers, columns)
        self.assertEqual(tuple(self.datastore_data), tuple(data))