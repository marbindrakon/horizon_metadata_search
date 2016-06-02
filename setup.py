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

import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('test-requirements.txt') as f:
    required_for_tests = f.read().splitlines()

setup(
    name='horizon_metadata_search',
    version='0.1',
    packages=[
        'metasearchdashboard', 'metasearchdashboard.metafinder',
        'metasearchdashboard.metafinder.api', 'metasearchdashboard.enabled'
    ],
    package_data={
        'metasearchdashboard': [
            'static/metasearch/js/*',
            'static/metasearch/scss/*',
            'templates/metasearch/*.html',
            'enabled/*.py'
        ],
        'metasearchdashboard.metafinder': [
            'templates/metafinder/*.html'
        ],
    },
    install_requires=required,
    license='License :: OSI Approved :: Apache Software License',
    classifiers=[
        'Environment :: OpenStack',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://github.com/michaelrice/horizon_metadata_search',
    author='Michael Rice',
    author_email='michael.rice@rackspace.com',
    description='Metadata search dashboard for Horizon',
    long_description=read('README.rst'),
    zip_safe=False,
)
