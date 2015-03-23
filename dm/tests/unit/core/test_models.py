# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2014 Eugene Frolov <eugene@frolov.net.ru>
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import six

from dm.core import models
from dm.core import properties
from dm.tests.unit import base


class FakeProperty(mock.Mock):
    pass


FAKE_PROPERTY1 = FakeProperty()
FAKE_PROPERTY2 = FakeProperty()
FAKE_VALUE1 = 'Fake value 1'


class MetaModelTestCase(base.BaseTestCase):

    with mock.patch('dm.core.properties.PropertyCreator', FakeProperty):

        @six.add_metaclass(models.MetaModel)
        class Model(object):

            fake_prop1 = FAKE_PROPERTY1
            fake_prop2 = FAKE_PROPERTY2

    def test_model_class(self):
        self.assertIsInstance(self.Model.properties,
                              properties.PropertyCollection)

    def test_metamodel_getattr(self):
        self.assertNotEqual(self.Model.fake_prop1, FAKE_PROPERTY1)
        self.assertNotEqual(self.Model.fake_prop2, FAKE_PROPERTY2)

    def test_metamodel_getattr_raises_attribute_error(self):
        self.assertRaises(AttributeError, lambda: self.Model.fake_prop3)


class ModelTestCase(base.BaseTestCase):

    PM_MOCK = mock.MagicMock(name='PropertyManager object')

    @mock.patch('dm.core.properties.PropertyManager', return_value=PM_MOCK)
    def setUp(self, pm_mock):
        super(ModelTestCase, self).setUp()
        self.PM_MOCK.__getitem__.side_effect = None
        self.PM_MOCK.reset_mock()
        self.pm_mock = pm_mock
        self.kwargs = {'kwarg1': 1, 'kwarg2': 2}
        self.test_instance = models.Model(**self.kwargs)

    def test_obj(self):
        self.assertEqual(self.test_instance.properties, self.PM_MOCK)
        self.pm_mock.assert_called_once_with(models.Model.properties,
                                             **self.kwargs)

    def test_obj_getattr(self):
        self.assertEqual(self.test_instance.fake_prop1,
                         self.PM_MOCK['fake_prop1'].value)

    def test_obj_getattr_raise_attribute_error(self):
        self.PM_MOCK.__getitem__.side_effect = KeyError

        self.assertRaises(AttributeError,
                          lambda: self.test_instance.fake_prop1)

    def test_obj_setattr(self):
        self.test_instance.fake_prop1 = FAKE_VALUE1

        self.assertEqual(self.PM_MOCK.__getitem__().value, FAKE_VALUE1)
