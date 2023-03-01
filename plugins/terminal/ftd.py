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
#from __future__ import absolute_import, division, print_function
#__metaclass__ = type # no more Py2

#DOCUMENTAION = ... see ../cliconf/...

import re
import json

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text, to_bytes
from ansible.plugins.terminal import TerminalBase


class TerminalModule(TerminalBase):

    # banner re.compile(br"^(\r\n)?(Restricted area[\r\n]?)?(\([a-zA-Z0-9_@.]+\ )Password )$")
    terminal_stdout_re = [ # also can be set in a play as var ansible_terminal_stdout_re.{pattern,flags}
        re.compile(br"(^|\r\n)+> $")
    ]

    terminal_stderr_re = [ # also can be set in a play...
        re.compile(br"(^|\r\n)Syntax error:\s[\S ]+(\r\n|$)"),
        #re.compile(br"(^|\r\n)Epert mode is not available for direct ssh sessions\.((\r\n).)+(\r\n)Note, expert mode access can be granted by FXOS administrator\.(?=(\r\n)>\s)", re.M),
        re.compile(br"(^|\r\n)Password:\s") # Falling out of privileges.
    ]

    #def on_open_shell(self):
    #    try:
    #        for cmd in (b'terminal page disable', b'terminal redisp off', b'terminal width 256'):
    #            self._exec_cli_command(cmd)
    #    except AnsibleConnectionFailure:
    #        raise AnsibleConnectionFailure('unable to set terminal parameters')

    #def on_become(self, passwd=None):
    #    if self._get_prompt().endswith(b'#'):
    #        return

    #    cmd = {u'command': u'su'}
    #    if passwd:
    #        # Note: python-3.5 cannot combine u"" and r"" together.  Thus make
    #        # an r string and use to_text to ensure it's text on both py2 and py3.
    #        cmd[u'prompt'] = to_text(r"[\r\n]Password: $", errors='surrogate_or_strict')
    #        cmd[u'answer'] = passwd
    #        cmd[u'prompt_retry_check'] = True
    #    try:
    #        self._exec_cli_command(to_bytes(json.dumps(cmd), errors='surrogate_or_strict'))
    #        prompt = self._get_prompt()
    #        if prompt is None or not prompt.endswith(b' '):
    #            raise AnsibleConnectionFailure('failed to elevate privilege to enable mode still at prompt [%s]' % prompt)
    #    except AnsibleConnectionFailure as e:
    #        prompt = self._get_prompt()
    #        raise AnsibleConnectionFailure('unable to elevate privilege to enable mode, at prompt [%s] with error: %s' % (prompt, e.message))

    #    try:
    #        for cmd in (b'terminal page disable', b'terminal redisp off', b'terminal width 256'):
    #            self._exec_cli_command(cmd)
    #    except AnsibleConnectionFailure:
    #        raise AnsibleConnectionFailure('unable to set root terminal parameters')

    #def on_unbecome(self):
    #    prompt = self._get_prompt()
    #    if prompt is None:
    #        # if prompt is None most likely the terminal is hung up at a prompt
    #        return

    #    if b'# ' in prompt:
    #        self._exec_cli_command(b'exit')

    #    elif prompt.endswith(b'# '):
    #        self._exec_cli_command(b'exit ')
