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

async def reader(socket):
    while True:
        print('receiving...')
        value = await socket.recv()
        print('received:', value[:10])

socket = aionn.Socket(aionn.AF_SP, aionn.SUB)
socket.bind('tcp://*:5555')
socket.setsockopt(aionn.SUB, aionn.SUB_SUBSCRIBE, 'topic')
loop = asyncio.get_event_loop()
loop.run_until_complete(reader(socket))

# vim: sw=4:et:ai
