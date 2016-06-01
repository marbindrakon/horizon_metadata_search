#   Copyright 2016 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.metasearch.metafinder import tables

from openstack_dashboard.dashboards.metasearch.metafinder.api import swift_helpers


class PagedTableMixin(object):
    def __init__(self, *args, **kwargs):
        super(PagedTableMixin, self).__init__(*args, **kwargs)
        self._has_prev_data = False
        self._has_more_data = False

    def has_prev_data(self, table):
        return self._has_prev_data

    def has_more_data(self, table):
        return self._has_more_data

    def _get_marker(self):
        meta = self.table_classes[0]._meta
        prev_marker = self.request.GET.get(meta.prev_pagination_param, None)
        if prev_marker:
            return prev_marker, "asc"
        else:
            marker = self.request.GET.get(meta.pagination_param, None)
            if marker:
                return marker, "desc"
            return None, "desc"


class InstanceTab(PagedTableMixin, tabs.TableTab):
    name = _("Instances Tab")
    slug = "instances_tab"
    table_classes = (tables.InstancesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker, sort_dir = self._get_marker()

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class VolumeTab(PagedTableMixin, tabs.TableTab):
    name = _("Volumes Tab")
    slug = "volumes_tab"
    table_classes = (tables.VolumeTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    _has_more = False

    def has_more_data(self, table):
        return self._has_more

    def get_volumes_data(self):
        try:
            marker, sort_dir = self._get_marker()

            volumes, self._has_more, self._has_prev_data = api.cinder.volume_list_paged(
                self.request,
                marker=marker,
                paginate=True,
                search_opts=None
            )

            return volumes
        except Exception as e:
            self._has_more = False
            self._has_prev_data = False
            error_message = _('Unable to get volumes {}.'.format(e.message))
            exceptions.handle(self.request, error_message)

            return []


class ImageTab(PagedTableMixin, tabs.TableTab):
    name = _("Images Tab")
    slug = "images_tab"
    table_classes = (tables.ImageTable, )

    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_images_data(self):
        try:
            marker, sort_dir = self._get_marker()

            images, self._has_more, self._has_prev_data = api.glance.image_list_detailed(
                self.request,
                marker=marker,
                filters=None, paginate=True)

            return images
        except Exception as e:
            self._has_more = False
            self._has_prev_data = False
            error_message = _('Unable to get images {}.'.format(e.message))
            exceptions.handle(self.request, error_message)

            return []


class ContainerTab(PagedTableMixin, tabs.TableTab):
    name = _("Container Tab")
    slug = "containers_tab"
    table_classes = (tables.ContainerTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_containers_data(self):
        try:
            marker, sort_dir = self._get_marker()
            containers, self._has_more = api.swift.swift_get_containers(
                request=self.request,
                marker=marker
            )
            nc = []
            for c in containers:
                cc = swift_helpers.swift_get_container_with_metadata(self.request, c.name)
                nc.append(cc)
            n = len(containers)
            for c in nc:
                c.id = n
                n -= 1
            return nc
        except Exception as e:
            self._has_more = False
            self._has_prev_data = False
            error_message = _('Unable to get containers {}.'.format(e.message))
            exceptions.handle(self.request, error_message)
            return []


class MetaFinderTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (InstanceTab, VolumeTab, ImageTab, ContainerTab)
    sticky = True
