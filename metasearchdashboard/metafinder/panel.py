# Copyright 2016 Rackspace
#
# Author: Michael Rice <michael.rice@rackspace.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

import horizon
from metasearchdashboard import dashboard


class Metafinder(horizon.Panel):
    name = _("Find By Metadata")
    slug = "metafinder"


dashboard.Metasearch.register(Metafinder)
