# -*- encoding: utf-8 -*-
# Copyright (c) 2015 b<>com
#
# Authors: Jean-Emile DARTOIS <jean-emile.dartois@b-com.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from concurrent.futures import ThreadPoolExecutor

from oslo_config import cfg
from oslo_log import log

from watcher.applier.messaging.trigger import TriggerActionPlan
from watcher.common.messaging.messaging_core import MessagingCore

LOG = log.getLogger(__name__)
CONF = cfg.CONF

# Register options
APPLIER_MANAGER_OPTS = [
    cfg.IntOpt('applier_worker', default='1', help='The number of worker'),
    cfg.StrOpt('topic_control',
               default='watcher.applier.control',
               help='The topic name used for'
                    'control events, this topic '
                    'used for rpc call '),
    cfg.StrOpt('topic_status',
               default='watcher.applier.status',
               help='The topic name used for '
                    'status events, this topic '
                    'is used so as to notify'
                    'the others components '
                    'of the system'),
    cfg.StrOpt('publisher_id',
               default='watcher.applier.api',
               help='The identifier used by watcher '
                    'module on the message broker')
]

opt_group = cfg.OptGroup(name='watcher_applier',
                         title='Options for the Applier messaging'
                               'core')
CONF.register_group(opt_group)
CONF.register_opts(APPLIER_MANAGER_OPTS, opt_group)


class ApplierManager(MessagingCore):
    def __init__(self):
        super(ApplierManager, self).__init__(
            CONF.watcher_applier.publisher_id,
            CONF.watcher_applier.topic_control,
            CONF.watcher_applier.topic_status,
            api_version=self.API_VERSION,
        )
        # shared executor of the workflow
        self.executor = ThreadPoolExecutor(max_workers=1)
        # trigger action_plan
        self.topic_control.add_endpoint(TriggerActionPlan(self))

    def join(self):
        self.topic_control.join()
        self.topic_status.join()
