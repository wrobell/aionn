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
import nnpy

logger = logging.getLogger(__name__)

EAGAIN = 11

class Socket(nnpy.Socket):
    def __init__(self, domain, protocol, loop=None):
        super().__init__(domain, protocol)
        if loop == None:
            loop = asyncio.get_event_loop()
        self._loop = loop

        self._reader = asyncio.Queue(loop=loop)
        self._fd_reader = None
        self._read_flags = 0

        self._writer = asyncio.Event(loop=loop)
        self._fd_writer = None
        self._write_flags = 0

    async def recv(self, flags=0):
        self._read_flags = flags | nnpy.DONTWAIT
        self._enable_reader()
        value = await self._reader.get()
        return value

    async def send(self, data, flags=0):
        self._data = data
        self._write_flags = flags | nnpy.DONTWAIT
        self._enable_writer()
        await self._writer.wait()

    def _notify_recv(self):
        self._loop.remove_reader(self._fd_reader)
        result = super().recv(self._read_flags)
        self._reader.put_nowait(result)

    def _notify_send(self):
        try:
            self._loop.remove_writer(self._fd_writer)
            super().send(self._data, self._write_flags)
            self._writer.set()
            self._writer.clear()
        except nnpy.NNError as ex:
            if ex.error_no == EAGAIN:
                # avoid blocking sender by delaying next write; in the
                # future, use NN_SNDTIMEO and allow the operation to
                # timeout; at the moment we use default timeout approach
                # (infinite timeout), see nn_setsockopt(3)/NN_SNDTIMEO
                if __debug__:
                    logger.debug('EAGAIN on send, delay sender')
                self._loop.call_later(1, self._enable_writer)
            else:
                raise
            
    def _enable_reader(self):
        self._fd_reader = self.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)
        self._loop.add_reader(self._fd_reader, self._notify_recv)

    def _enable_writer(self):
        self._fd_writer = self.getsockopt(nnpy.SOL_SOCKET, nnpy.SNDFD)
        self._loop.add_writer(self._fd_writer, self._notify_send)

# vim: sw=4:et:ai
