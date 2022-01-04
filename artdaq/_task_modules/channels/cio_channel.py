from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import lib_importer, ctypes_byte_str
from artdaq._task_modules.channels.channel import Channel
from artdaq.constants import Edge
from artdaq.errors import (check_for_error)


class CIOChannel(Channel):
    """
    Represents one or more counter input virtual channels and their properties.
    """
    __slots__ = []

    def __repr__(self):
        return 'CIOChannel(name={0})'.format(self._name)

    @property
    def ci_meas_type(self):
        """
        :class:`artdaq.constants.UsageTypeCI`: Indicates the
            measurement to take with the channel.
        """
        return 0

    def cfg_ci_count_edges_count_reset(
            self, source="", reset_count=0, active_edge=Edge.RISING, dig_fltr_min_pulse_width=0.0):

        """
        reset edge count at the ci countEdges mode
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgCICountEdgesCountReset
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str, ctypes.c_uint,
                        ctypes.c_int, ctypes.c_double]

        error_code = cfunc(
            self._handle, source, reset_count, active_edge.value, dig_fltr_min_pulse_width)
        check_for_error(error_code)

    def ci_count_edges_count_reset_disable(self):
        cfunc = lib_importer.windll.ArtDAQ_DisableCICountEdgesCountReset
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle]

        error_code = cfunc(self._handle)
        check_for_error(error_code)

    @property
    def co_output_type(self):
        """
        :class:`artdaq.constants.UsageTypeCO`: Indicates how to define
            pulses generated on the channel.
        """
        return 0