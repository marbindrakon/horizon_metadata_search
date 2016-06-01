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
from django.core.urlresolvers import reverse
from django.conf import settings

from openstack_dashboard.dashboards.project.containers import utils
from openstack_dashboard.dashboards.project.instances.tables import \
    DeleteInstance, RebootInstance, SoftRebootInstance, \
    TogglePause, ToggleSuspend, ToggleShelve, LaunchLink, LaunchLinkNG, \
    EditInstance, EditInstanceSecurityGroups, CreateSnapshot, ConsoleLink, \
    LogLink, ResizeLink, ConfirmResize, RevertResize, RebuildInstance, \
    DecryptInstancePassword, AssociateIP, SimpleAssociateIP, \
    SimpleDisassociateIP, UpdateMetadata, UpdateRow, StartInstance, \
    StopInstance, LockInstance, UnlockInstance, AttachInterface, \
    DetachInterface, TASK_DISPLAY_NONE, TASK_DISPLAY_CHOICES

from openstack_dashboard.dashboards.project.volumes.volumes.tables import \
    EditVolume, ExtendVolume, LaunchVolume, LaunchVolumeNG, EditAttachments, \
    CreateBackup, CreateSnapshot, RetypeVolume, UploadToImage, \
    CreateTransfer, DeleteTransfer, DeleteVolume, AcceptTransfer, CreateVolume

from openstack_dashboard.dashboards.project.images.images.tables import \
    CreateImage, DeleteImage, LaunchImage, LaunchImageNG, \
    CreateVolumeFromImage, EditImage
from openstack_dashboard.dashboards.project.images.images.tables import \
    UpdateMetadata as UpdateMetadataImg

from horizon import tables


class MetadataFilterAction(tables.FilterAction):
    name = "metadatafilter"


def metadata_dict_to_str(metadata, attr_name=None):
    """
    Returns the metadata dict into a string

    Ex:
    metadata = {"app_id": "myapp", "color": "blue"}
    return "app_id: myapp, color: blue"
    """
    attr_name = attr_name or "metadata"
    metadata = getattr(metadata, attr_name)
    if metadata is None:
        return "None"
    mystr = ""
    items = len(metadata)
    for k, v in metadata.iteritems():
        mystr += "{}: {}".format(k, v)
        items -= 1
        if items >= 1:
            mystr += ", "
    return mystr


class InstancesTable(tables.DataTable):
    TASK_STATUS_CHOICES = (
        (None, True),
        ("none", True)
    )
    STATUS_CHOICES = (
        ("active", True),
        ("shutoff", True),
        ("suspended", True),
        ("paused", True),
        ("error", False),
        ("rescue", True),
        ("shelved", True),
        ("shelved_offloaded", True),
    )
    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:admin:instances:detail")
    status = tables.Column("status", verbose_name=_("Status"))
    task = tables.Column("OS-EXT-STS:task_state",
                         verbose_name=_("Task"),
                         empty_value=TASK_DISPLAY_NONE,
                         status=True,
                         status_choices=TASK_STATUS_CHOICES,
                         display_choices=TASK_DISPLAY_CHOICES)
    zone = tables.Column('availability_zone',
                         verbose_name=_("Availability Zone"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))
    meta_data = tables.Column(metadata_dict_to_str, verbose_name=_("Metadata"))

    class Meta(object):
        name = "instances"
        verbose_name = _("Instances")
        status_columns = ["status", "task"]
        row_class = UpdateRow
        table_actions_menu = (StartInstance, StopInstance, SoftRebootInstance)
        launch_actions = ()
        if getattr(settings, 'LAUNCH_INSTANCE_LEGACY_ENABLED', False):
            launch_actions = (LaunchLink,) + launch_actions
        if getattr(settings, 'LAUNCH_INSTANCE_NG_ENABLED', True):
            launch_actions = (LaunchLinkNG,) + launch_actions
        table_actions = launch_actions + (MetadataFilterAction, DeleteInstance)
        row_actions = (StartInstance, ConfirmResize, RevertResize,
                       CreateSnapshot, SimpleAssociateIP, AssociateIP,
                       SimpleDisassociateIP, AttachInterface,
                       DetachInterface, EditInstance, UpdateMetadata,
                       DecryptInstancePassword, EditInstanceSecurityGroups,
                       ConsoleLink, LogLink, TogglePause, ToggleSuspend,
                       ToggleShelve, ResizeLink, LockInstance, UnlockInstance,
                       SoftRebootInstance, RebootInstance,
                       StopInstance, RebuildInstance, DeleteInstance)
        pagination_param = 'instance_marker'
        prev_pagination_param = 'prev_instance_marker'


class VolumeTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:admin:volumes:volumes:detail")
    # status = tables.Column("status", verbose_name=_("Status"))
    # zone = tables.Column('availability_zone',
    #                      verbose_name=_("Availability Zone"))
    # image_name = tables.Column('image_name', verbose_name=_("Image Name"))
    availability_zone = tables.Column('availability_zone', verbose_name=_("Zone"))
    metadata = tables.Column(metadata_dict_to_str, verbose_name=_("Metadata"))

    class Meta(object):
        name = "volumes"
        verbose_name = _("Volumes")
        table_actions = (MetadataFilterAction, CreateVolume, AcceptTransfer, DeleteVolume)
        launch_actions = ()
        if getattr(settings, 'LAUNCH_INSTANCE_LEGACY_ENABLED', False):
            launch_actions = (LaunchVolume,) + launch_actions
        if getattr(settings, 'LAUNCH_INSTANCE_NG_ENABLED', True):
            launch_actions = (LaunchVolumeNG,) + launch_actions
        row_actions = ((EditVolume, ExtendVolume,) +
                       launch_actions +
                       (EditAttachments, CreateSnapshot, CreateBackup,
                        RetypeVolume, UploadToImage, CreateTransfer,
                        DeleteTransfer, DeleteVolume))
        pagination_param = 'volume_marker'
        prev_pagination_param = 'prev_volume_marker'


def images_md_to_str(data):
    return metadata_dict_to_str(data, attr_name="properties")


class ImageTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:admin:images:detail")
    properties = tables.Column(images_md_to_str, verbose_name=_("Metadata"))

    class Meta(object):
        name = "images"
        verbose_name = _("Images")
        table_actions = (MetadataFilterAction, CreateImage, DeleteImage, )
        launch_actions = ()
        if getattr(settings, 'LAUNCH_INSTANCE_LEGACY_ENABLED', False):
            launch_actions = (LaunchImage,) + launch_actions
        if getattr(settings, 'LAUNCH_INSTANCE_NG_ENABLED', True):
            launch_actions = (LaunchImageNG,) + launch_actions
        row_actions = launch_actions + (CreateVolumeFromImage,
                                        EditImage, UpdateMetadataImg,
                                        DeleteImage,)
        pagination_param = 'image_marker'
        prev_pagination_param = 'prev_image_marker'


def get_container_link(container):
    return reverse("horizon:project:containers:index",
                   args=(utils.wrap_delimiter(container.name),))


class ContainerTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"),
                         link=get_container_link)
    metadata = tables.Column(metadata_dict_to_str, verbose_name=_("Metadata"))

    class Meta(object):
        name = "containers"
        verbose_name = _("Containers")
        table_actions = (MetadataFilterAction, )
        pagination_param = 'container_marker'
        prev_pagination_param = 'prev_container_marker'
