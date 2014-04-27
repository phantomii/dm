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

import uuid

import six

from dm.core import types
from dm.tests.unit import base


class UUIDTestCase(base.BaseTestCase):

    def setUp(self):
        super(UUIDTestCase, self).setUp()
        self.test_instance = types.UUID()

    def test_uuid_correct_value(self):

        self.assertTrue(self.test_instance.validate(uuid.uuid4()))

    def test_uuid_incorrect_value(self):
        INCORECT_UUID = '4a775g98-eg85-4a0e-a0g0-639f0a16f4c3'

        self.assertFalse(self.test_instance.validate(
            INCORECT_UUID))

    def test_to_simple_type(self):
        TEST_UUID = uuid.uuid4()

        self.assertEqual(
            self.test_instance.to_simple_type(TEST_UUID),
            str(TEST_UUID))

    def test_from_simple_type(self):
        TEST_UUID = uuid.uuid4()

        self.assertEqual(
            self.test_instance.from_simple_type(str(TEST_UUID)),
            TEST_UUID)


class StringTestCase(base.BaseTestCase):

    FAKE_STRING1 = 'fake!!!'
    FAKE_STRING2 = six.u('fake!!!')

    def setUp(self):
        super(StringTestCase, self).setUp()
        self.test_instance1 = types.String(min_length=5, max_length=8)
        self.test_instance2 = types.String()

    def test_correct_value(self):
        self.assertTrue(self.test_instance1.validate(self.FAKE_STRING1))

    def test_correct_unicode_value(self):
        self.assertTrue(self.test_instance1.validate(self.FAKE_STRING2))

    def test_correct_min_value(self):
        self.assertTrue(self.test_instance1.validate(self.FAKE_STRING1[:5]))

    def test_correct_min_unicode_value(self):
        self.assertTrue(self.test_instance1.validate(self.FAKE_STRING2[:5]))

    def test_correct_max_value(self):
        self.assertTrue(self.test_instance1.validate(
            (self.FAKE_STRING1 * 2)[:8]))

    def test_correct_max_unicode_value(self):
        self.assertTrue(self.test_instance1.validate(
            (self.FAKE_STRING2 * 2)[:8]))

    def test_incorrect_min_value(self):
        self.assertFalse(self.test_instance1.validate(self.FAKE_STRING1[:4]))

    def test_incorrect_min_unicode_value(self):
        self.assertFalse(self.test_instance1.validate(self.FAKE_STRING1[:4]))

    def test_incorrect_max_value(self):
        self.assertFalse(self.test_instance1.validate(
            (self.FAKE_STRING1 * 2)[:9]))

    def test_incorrect_max_unicode_value(self):
        self.assertFalse(self.test_instance1.validate(
            (self.FAKE_STRING1 * 2)[:9]))

    def test_correct_infinity_value(self):
        self.assertTrue(self.test_instance2.validate(
            self.FAKE_STRING1 * 100500))

    def test_incorrect_type_validate(self):
        self.assertFalse(self.test_instance1.validate(5))


class IntegerTestCase(base.BaseTestCase):

    def setUp(self):
        super(IntegerTestCase, self).setUp()

        self.test_instance = types.Integer(0, 55)

    def test_validate_correct_value(self):
        self.assertTrue(self.test_instance.validate(30))

    def test_validate_correct_max_value(self):
        self.assertTrue(self.test_instance.validate(55))

    def test_validate_correct_min_value(self):
        self.assertTrue(self.test_instance.validate(0))

    def test_validate_incorrect_value(self):
        self.assertFalse(self.test_instance.validate("TEST_STR_VALUE"))

    def test_validate_incorrect_max_value(self):
        self.assertFalse(self.test_instance.validate(56))

    def test_validate_incorrect_min_value(self):
        self.assertFalse(self.test_instance.validate(-1))

    def test_validate_sys_max_value(self):
        test_instance = types.Integer()

        self.assertTrue(test_instance.validate(six.MAXSIZE))

    def test_validate_sys_min_value(self):
        test_instance = types.Integer()

        self.assertTrue(test_instance.validate(-six.MAXSIZE))
