#!/usr/bin/env python

# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sahara.utils import patches
patches.patch_all()

import gettext
import os
import sys

import eventlet
from eventlet import wsgi
from oslo.config import cfg


# If ../sahara/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir,
                               'sahara',
                               '__init__.py')):
    sys.path.insert(0, possible_topdir)

gettext.install('sahara', unicode=1)


import sahara.main as server
from sahara.openstack.common import log as logging


LOG = logging.getLogger(__name__)


def main():
    server.setup_common(possible_topdir, 'all-in-one')

    app = server.make_app()

    server.setup_sahara_api(app, 'all-in-one')
    server.setup_sahara_engine()

    wsgi.server(eventlet.listen((cfg.CONF.host, cfg.CONF.port), backlog=500),
                app, log=logging.WritableLogger(LOG), debug=False)
