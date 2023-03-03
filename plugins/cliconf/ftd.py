# Copyright (c) 2023 Alexander.Kross@gmail.com all rights reserved.
#
# (c) 2017 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
#from __future__ import (absolute_import, division, print_function)
#__metaclass__ = type # no more Py2

# See also well documented example at https://github.com/nokia/ansible-networking-collections/blob/master/sros/plugins/cliconf/classic.py

DOCUMENTATION = """
author: Alexander.Kross@gmail.com
cliconf: ftd
short_description: Use ftd cliconf to run command on Cisco FTD instances
description:
- This ftd plugin provides low level abstraction apis for sending and receiving CLI
  commands from Cisco Firepower Threat Defense (FTD) instances.
version_added: 1.0.0
"""

import re
import time
import json

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.config import (
    NetworkConfig,
    dumps,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    to_list,
)
from ansible.plugins.cliconf import CliconfBase, enable_mode


class Cliconf(CliconfBase):

    @enable_mode
    def get_config(self, source='running', flags=None, format=None):
        if source not in ('running', 'startup'):
            raise ValueError("fetching configuration from %s is not supported" % source)

        if format:
            raise ValueError("'format' value %s is not supported for get_config" % format)

        if not flags:
            flags = []
        if source == 'running':
            cmd = 'show running-config '
        else:
            cmd = 'show startup-config '

        cmd += ' '.join(to_list(flags))
        cmd = cmd.strip()

        return self.send_command(cmd)

    @enable_mode
    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        resp = {}
        operations = self.get_device_operations()
        self.check_edit_config_capability(operations, candidate, commit, replace, comment)

        results = []
        requests = []
        if commit:
            for line in to_list(candidate):
                if not isinstance(line, Mapping):
                    line = {'command': line}

                cmd = line['command']
                if cmd != 'end' and cmd[0] != '!':
                    results.append(self.send_command(**line))
                    requests.append(cmd)
        else:
            raise ValueError('check mode is not supported')

        resp['request'] = requests
        resp['response'] = results
        return resp

    def edit_macro(self, candidate=None, commit=True, replace=None, comment=None):
        resp = {}
        operations = self.get_device_operations()
        self.check_edit_config_capabiltiy(operations, candidate, commit, replace, comment)

        results = []
        requests = []
        if commit:
            commands = ''
            for line in candidate:
                if line != 'None':
                    commands += (' ' + line + '\n')
                obj = {'command': commands, 'sendonly': True}
                results.append(self.send_command(**obj))
                requests.append(commands)

            time.sleep(0.1)
            results.append(self.send_command('\n'))
            requests.append('\n')

        resp['request'] = requests
        resp['response'] = results
        return resp

    def get(self, command=None, prompt=None, answer=None, sendonly=False, output=None, newline=True, check_all=False):
        if not command:
            raise ValueError('must provide value of command to execute')
        if output:
            raise ValueError("'output' value %s is not supported for get" % output)

        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, newline=newline, check_all=check_all)

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'ftd'
        reply = self.get(command='show version')
        data = to_text(reply, errors='surrogate_or_strict').strip()

        match = re.search(r'Model                     : Cisco Firepower (\d+) Threat Defense \((\d+)\) Version ([\d.]+) \(Build (\d+)\)', data)
        device_info['network_os_version'] = match.group(3) if match else "Error: cannot parse Model line of ``show version`` command."

        return device_info

    def get_device_operations(self):
        return {
            'supports_diff_replace': False,
            'supports_commit': False,
            'supports_rollback': False,
            'supports_defaults': True,
            'supports_onbox_diff': False,
            'supports_commit_comment': False,
            'supports_multiline_delimiter': False,
            'supports_diff_match': False,
            'supports_diff_ignore_lines': False,
            'supports_generate_diff': False,
            'supports_replace': False
        }

    def get_option_values(self):
        return {
            'format': ['text'],
            'diff_match': ['line', 'none'],
            'diff_replace': [],
            'output': []
        }

    def get_capabilities(self):
        result = dict()
        result['rpc'] = self.get_base_rpc() + ['run_commands'] #+ ['edit_banner', 'get_diff', 'get_defaults_flag']
        result['network_api'] = 'cliconf'
        result['device_info'] = self.get_device_info()
        result['device_operations'] = self.get_device_operations()
        result.update(self.get_option_values())
        return json.dumps(result)

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        responses = list()
        for cmd in to_list(commands):
            if not isinstance(cmd, Mapping):
                cmd = {'command': cmd}

            output = cmd.pop('output', None)
            if output:
                raise ValueError("'output' value %s is not supported for run_commands" % output)

            try:
                out = self.send_command(**cmd)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, 'err', to_text(e))

            responses.append(out)

        return responses

    def get_defaults_flag(self):
        """
        The method identifies the filter that should be used to fetch running-configuration
        with defaults.
        :return: valid default filter
        """
        out = self.get('show config running ?')
        out = to_text(out, errors='surrogate_then_replace')

        commands = set()
        for line in out.splitlines():
            if line.strip():
                commands.add(line.strip().split()[0])

        if 'all' in commands:
            return 'all'
        else:
            return 'full'
