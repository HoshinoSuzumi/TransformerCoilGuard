from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import lib_importer, c_bool32
from artdaq._task_modules.channels.channel import Channel
from artdaq.constants import OverwriteMode
from artdaq.errors import check_for_error, is_string_buffer_too_small


class InStream(object):
    """
    Exposes an input data stream on a DAQ task.

    The input data stream be used to control reading behavior and can be
    used in conjunction with reader classes to read samples from an
    DAQ task.
    """
    def __init__(self, task):
        self._task = task
        self._handle = task._handle
        self._timeout = 10.0

        super(InStream, self).__init__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._handle == other._handle and
                    self._timeout == other._timeout)
        return False

    def __hash__(self):
        return hash((self._handle.value, self._timeout))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'InStream(task={0})'.format(self._task.name)

    @property
    def timeout(self):
        """
        float: Specifies the amount of time in seconds to wait for
            samples to become available. If the time elapses, the read
            method returns an error and any samples read before the
            timeout elapsed. The default timeout is 10 seconds. If you
            set timeout to artdaq.WAIT_INFINITELY, the read method
            waits indefinitely. If you set timeout to 0, the read method
            tries once to read the requested samples and returns an error
            if it is unable to.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        self._timeout = val

    @timeout.deleter
    def timeout(self):
        self._timeout = 10.0

    @property
    def auto_start(self):
        """
        bool: Specifies if DAQ Read automatically starts the task  if
            you did not start the task explicitly by using DAQ Start.
            The default value is True. When  DAQ Read starts a finite
            acquisition task, it also stops the task after reading the
            last sample.
        """
        val = c_bool32()

        cfunc = lib_importer.windll.ArtDAQ_GetReadAutoStart
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.POINTER(c_bool32)]

        error_code = cfunc(
            self._handle, ctypes.byref(val))
        check_for_error(error_code)

        return val.value

    @auto_start.setter
    def auto_start(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetReadAutoStart
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, c_bool32]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    @property
    def channels_to_read(self):
        """
        :class:`artdaq._task_modules.channels.channel.Channel`:
            Specifies a subset of channels in the task from which to
            read.
        """
        cfunc = lib_importer.windll.ArtDAQ_GetTaskAttribute
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int, ctypes.c_char_p,
                        ctypes.c_int]

        temp_size = 256
        while True:
            val = ctypes.create_string_buffer(temp_size)

            size_or_code = cfunc(
                self._handle, 0x1273, val, temp_size)

            if is_string_buffer_too_small(size_or_code):
                # Buffer size must have changed between calls; check again.
                temp_size = 0
            elif size_or_code > 0 and temp_size == 0:
                # Buffer size obtained, use to retrieve data.
                temp_size = size_or_code
            else:
                break

        check_for_error(size_or_code)
        return Channel._factory(self._handle, val.value.decode('ascii'))

    def di_num_booleans_per_chan(self):
        """
        int: Indicates the number of booleans per channel that
            returns in a sample for line-based reads. If a channel has
            fewer lines than this number, the extra booleans are False.
        """
        return 1

    @property
    def over_write(self):
        """
        :class:`artdaq.constants.OverwriteMode`: Specifies whether to
            overwrite samples in the buffer that you have not yet read.
        """
        val = ctypes.c_int()

        cfunc = lib_importer.windll.ArtDAQ_GetReadOverWrite
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.POINTER(ctypes.c_int)]

        error_code = cfunc(
            self._handle, ctypes.byref(val))
        check_for_error(error_code)

        return OverwriteMode(val.value)

    @over_write.setter
    def over_write(self, val):
        val = val.value
        cfunc = lib_importer.windll.ArtDAQ_SetReadOverWrite
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)
