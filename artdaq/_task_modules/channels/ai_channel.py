from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import (
    lib_importer, ctypes_byte_str)
from artdaq._task_modules.channels.channel import Channel
from artdaq.errors import (check_for_error, is_string_buffer_too_small)


class AIChannel(Channel):
    """
    Represents one or more analog input virtual channels and their properties.
    """
    __slots__ = []

    def __repr__(self):
        return 'AIChannel(name={0})'.format(self._name)

    @property
    def ai_input_src(self):
        """
        str: Specifies the source of the channel. You can use the signal
            from the I/O connector or one of several calibration
            signals. Certain devices have a single calibration signal
            bus. For these devices, you must specify the same
            calibration signal for all channels you connect to a
            calibration signal.
        """
        cfunc = lib_importer.windll.ArtDAQ_GetAIInputSrc
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_char_p, ctypes.c_uint]

        temp_size = 0
        while True:
            val = ctypes.create_string_buffer(temp_size)

            size_or_code = cfunc(
                self._handle, self._name, val, temp_size)

            if is_string_buffer_too_small(size_or_code):
                # Buffer size must have changed between calls; check again.
                temp_size = 0
            elif size_or_code > 0 and temp_size == 0:
                # Buffer size obtained, use to retrieve data.
                temp_size = size_or_code
            else:
                break

        check_for_error(size_or_code)

        return val.value.decode('ascii')

    @ai_input_src.setter
    def ai_input_src(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetAIInputSrc
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str]

        error_code = cfunc(
            self._handle, self._name, val)
        check_for_error(error_code)