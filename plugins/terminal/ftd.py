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
