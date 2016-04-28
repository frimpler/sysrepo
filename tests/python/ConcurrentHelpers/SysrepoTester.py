#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Rastislav Szabo <raszabo@cisco.com>, Lukas Macko <lmacko@cisco.com>"
__copyright__ = "Copyright 2016, Cisco Systems, Inc."
__license__ = "Apache 2.0"

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ConcurrentHelpers import *
from SysrepoWrappers import *


class SysrepoTester(Tester):
    def __init__(self, name="LockUser", ds=SR_DS_STARTUP, conn=SR_CONN_DEFAULT, connectInSetup=True):
        super(SysrepoTester, self).__init__()
        self.name = name
        self.ds = ds
        self.conn = conn
        self.autoconnect = connectInSetup

    def setup(self):
        if self.autoconnect:
            self.sr = Sysrepo(self.name, self.conn)
            self.session = Session(self.sr, self.ds)
            self.sr.log_stderr(SR_LL_INF)

    def restartConnection(self):
        self.sr = Sysrepo(self.name, self.conn)
        self.session = Session(self.sr, self.ds)

    def lockStep(self):
        self.session.lock_datastore()

    def lockFailStep(self):
        with self.tc.assertRaises(RuntimeError):
            self.session.lock_datastore()

    def unlockStep(self):
        self.session.unlock_datastore()

    def lockModelStep(self, module_name):
        self.session.lock_module(module_name)

    def lockFailModelStep(self, module_name):
        with self.tc.assertRaises(RuntimeError):
            self.session.lock_module(module_name)

    def unlockModelStep(self, module_name):
        self.session.unlock_module(module_name)

    def commitFailStep(self):
        with self.tc.assertRaises(RuntimeError):
            self.session.commit()

    def commitStep(self):
        self.session.commit()

    def getItemsStep(self, xpath):
        self.session.get_items(xpath)

    def getItemsFailStep(self, xpath):
        with self.tc.assertRaisesRegexp(RuntimeError, ".* found"):
            self.session.get_items(xpath)

    def refreshStep(self):
        self.session.refresh()