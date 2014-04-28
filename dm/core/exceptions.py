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


class DmException(Exception):
    """Base Domain Model Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        self.msg = self.message % kwargs
        super(DmException, self).__init__(self.msg)

    def __repr__(self):
        return "Message: %s" % self.msg


class PropertyRequired(DmException, ValueError):

    message = "Value is required! Property should not be None value."


class ReadOnlyProperty(DmException, ValueError):

    message = "Property is read only!"


class TypeError(DmException, TypeError):

    message = "Invalid type value '%(value)s' for '%(property_type)s'"

    def __init__(self, value, property_type):
        super(TypeError, self).__init__(
            value=value, property_type=type(property_type).__name__)
