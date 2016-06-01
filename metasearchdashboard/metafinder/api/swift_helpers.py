#   Copyright 2016 Rackspace
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

from datetime import datetime
import six.moves.urllib.parse as urlparse

from openstack_dashboard.api import base
from openstack_dashboard.api.swift import swift_api
from openstack_dashboard.api.swift import GLOBAL_READ_ACL
from openstack_dashboard.api.swift import Container


def swift_get_container_with_metadata(request, container_name, with_data=True):
    if with_data:
        headers, data = swift_api(request).get_object(container_name, "")
    else:
        data = None
        headers = swift_api(request).head_container(container_name)
    timestamp = None
    is_public = False
    public_url = None
    try:
        is_public = GLOBAL_READ_ACL in headers.get('x-container-read', '')
        if is_public:
            swift_endpoint = base.url_for(request,
                                          'object-store',
                                          endpoint_type='publicURL')
            parameters = urlparse.quote(container_name.encode('utf8'))
            public_url = swift_endpoint + '/' + parameters
        ts_float = float(headers.get('x-timestamp'))
        timestamp = datetime.utcfromtimestamp(ts_float).isoformat()
    except Exception:
        pass
    metadata = _headers_to_metadata(
        headers,
        meta_prefix='x-container-meta-',
        exclude_headers=(
            'content-type', 'content-length',
            'last-modified', 'etag', 'date',
            'x-object-manifest')
    )
    container_info = {
        'name': container_name,
        'container_object_count': headers.get('x-container-object-count'),
        'container_bytes_used': headers.get('x-container-bytes-used'),
        'timestamp': timestamp,
        'data': data,
        'is_public': is_public,
        'public_url': public_url,
        'metadata': metadata
    }
    return Container(container_info)


def _headers_to_metadata(headers, meta_prefix=None, exclude_headers=None):
    """
    """
    exclude_headers = exclude_headers or []
    meta_items = {}
    for key, value in headers.items():
        if key not in exclude_headers:
            if key.startswith(meta_prefix):
                meta_key = u'{}'.format(key[len(meta_prefix):])
                meta_items[meta_key] = value
    return meta_items
