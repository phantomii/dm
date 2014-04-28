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

import abc
import collections
import inspect
import six

from dm.core import exceptions as exc
from dm import utils


@six.add_metaclass(abc.ABCMeta)
class AbstractProperty(object):

    @abc.abstractproperty
    def value(self):
        pass

    @abc.abstractmethod
    def set_value_force(self, value):
        pass


class Property(AbstractProperty):

    def __init__(self, property_type, default=None, required=False,
                 read_only=False, value=None):
        self._type = (property_type() if inspect.isclass(property_type)
                      else property_type)
        self._required = bool(required)
        self._read_only = bool(read_only)
        default = default() if callable(default) else default
        self.set_value_force(value or default)

    def _safe_value(self, value):
        if value is None or self._type.validate(value):
            if value is None and self.is_required():
                raise exc.PropertyRequired()
            return value
        else:
            raise exc.TypeError(value=value, property_type=self._type)

    def is_read_only(self):
        return self._read_only

    def is_required(self):
        return self._required

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (self.is_read_only()):
            raise exc.ReadOnlyProperty()
        self._value = self._safe_value(value)

    def set_value_force(self, value):
        self._value = self._safe_value(value)


class PropertyCreator(object):

    def __init__(self, prop_class, args, kwargs):
        self._property = prop_class
        self._args = args
        self._kwargs = kwargs

    def __call__(self, value):
        return self._property(value=value, *self._args, **self._kwargs)

    def get_property_class(self):
        return self._property


@six.add_metaclass(abc.ABCMeta)
class PropertyMapping(collections.Mapping):

    @abc.abstractproperty
    def properties(self):
        pass

    def __getitem__(self, name):
        return self.properties[name]

    def __iter__(self):
        return six.iterkeys(self.properties)

    def __len__(self):
        return len(self.properties)


class PropertyCollection(PropertyMapping):

    def __init__(self, **kwargs):
        self._properties = kwargs
        super(PropertyCollection, self).__init__()

    def __getitem__(self, name):
        return self.properties[name].get_property_class()

    @property
    def properties(self):
        return utils.ReadOnlyDictProxy(self._properties)

    def __add__(self, other):
        if isinstance(other, PropertyCollection):
            props = dict(self.properties)
            props.update(other.properties)
            return type(self)(**props)
        raise TypeError("Cannot concatenate %s and %s objects" %
                        (type(self).__name__, type(other).__name__))

    def instantiate_property(self, name, value=None):
        return self._properties[name](value)


class PropertyManager(PropertyMapping):

    def __init__(self, property_collection, **kwargs):
        self._properties = {}
        for name in property_collection.properties.keys():
            self._properties[name] = property_collection.instantiate_property(
                name, kwargs.pop(name, None))
        if len(kwargs) > 0:
            raise TypeError("Unknown parameters: %s" % str(kwargs))
        super(PropertyManager, self).__init__()

    @property
    def properties(self):
        return utils.ReadOnlyDictProxy(self._properties)


def property(*args, **kwargs):
    PropertyClass = kwargs.pop('property_class', Property)
    if (inspect.isclass(PropertyClass) and
            issubclass(PropertyClass, AbstractProperty)):
        return PropertyCreator(PropertyClass, args=args, kwargs=kwargs)
    else:
        raise ValueError("Value of property class argument (%s) must be"
                         " inherited on AbstractProperty class"
                         "" % str(PropertyClass))
