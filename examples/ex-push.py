#!/usr/bin/env python
#
# aionn - asyncio messaging library based on nanomsg and nnpy
#
# Copyright (C) 2016 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import asyncio
import logging
import aionn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def writer(socket, delay=1):
    i = 0
    while True:
        await asyncio.sleep(delay)
        print('sending...')
        value = '{:04} '.format(i) + 'x' * 100
        await socket.send(value)
        print('sent', value[:10])
        i += 1

socket = aionn.Socket(aionn.AF_SP, aionn.PUSH)
socket.connect('tcp://localhost:5555')

loop = asyncio.get_event_loop()
loop.run_until_complete(writer(socket))

# vim: sw=4:et:ai
