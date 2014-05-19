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

from dm.core import exceptions
from dm.core import properties
from dm.core import types


class MetaModel(type):

    def __new__(cls, name, bases, attrs):
        props = {}
        for key, value in attrs.copy().items():
            if isinstance(value, properties.PropertyCreator):
                props[key] = value
                del attrs[key]
        attrs['properties'] = (attrs.pop('properties',
                                         properties.PropertyCollection()) +
                               properties.PropertyCollection(**props))
        return super(MetaModel, cls).__new__(cls, name, bases, attrs)

    def __getattr__(cls, name):
        try:
            return cls.properties[name]
        except KeyError:
            raise AttributeError("%s object has no attribute %s" % (
                cls.__name__, name))


@six.add_metaclass(MetaModel)
class Model(object):

    def __init__(self, **kwargs):
        self.properties = properties.PropertyManager(self.properties, **kwargs)

    def __getattr__(self, name):
        try:
            return self.properties[name].value
        except KeyError:
            raise AttributeError("%s object has no attribute %s" % (
                type(self).__name__, name))

    def __setattr__(self, name, value):
        try:
            self.properties[name].value = value
        except KeyError:
            super(Model, self).__setattr__(name, value)
        except exceptions.TypeError as e:
            raise exceptions.ModelTypeError(
                property_name=name,
                value=value,
                model=self,
                property_type=e.get_property_type())


class ModelWithUUID(Model):

    uuid = properties.property(types.UUID, read_only=True,
                               default=lambda: str(uuid.uuid4()))
