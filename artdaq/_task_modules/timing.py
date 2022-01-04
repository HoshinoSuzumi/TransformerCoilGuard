from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import lib_importer, ctypes_byte_str
from artdaq.constants import AcquisitionType, Edge
from artdaq.errors import check_for_error


class Timing(object):
    """
    Represents the timing configurations for a DAQ task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def ai_conv_src(self, val, active_edge=Edge.RISING):
        cfunc = lib_importer.windll.ArtDAQ_SetAIConvClk
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str, ctypes.c_int]

        error_code = cfunc(
            self._handle, val, active_edge.value)
        check_for_error(error_code)

    def samp_clk_timebase_src(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetSampClkTimebaseSrc
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    def samp_clk_timebase_outputterm(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetExportedSampClkTimebaseOutputTerm
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str]
        error_code = cfunc(
             self._handle, val)
        check_for_error(error_code)

    def ref_clk_src(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetRefClkSrc
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    def sync_pulse_src(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetSyncPulseSrc
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    def samp_sync_pulse_Event_outputterm(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetExportedSyncPulseEventOutputTerm
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str]
        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    def cfg_implicit_timing(
            self, sample_mode=AcquisitionType.FINITE, samps_per_chan=1000):
        """
        Sets only the number of samples to acquire or generate without
        specifying timing. Typically, you should use this instance when
        the task does not require sample timing, such as tasks that use
        counters for buffered frequency measurement, buffered period
        measurement, or pulse train generation. For finite counter
        output tasks, **samps_per_chan** is the number of pulses to
        generate.

        Args:
            sample_mode (Optional[artdaq.constants.AcquisitionType]): 
                Specifies if the task acquires or generates samples
                continuously or if it acquires or generates a finite
                number of samples.
            samps_per_chan (Optional[long]): Specifies the number of
                samples to acquire or generate for each channel in the
                task if **sample_mode** is **FINITE_SAMPLES**. If
                **sample_mode** is **CONTINUOUS_SAMPLES**, DAQ uses
                this value to determine the buffer size. This function
                returns an error if the specified value is negative.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgImplicitTiming
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int,
                        ctypes.c_ulonglong]

        error_code = cfunc(
            self._handle, sample_mode.value, samps_per_chan)
        check_for_error(error_code)

    def cfg_samp_clk_timing(
            self, rate, source="", active_edge=Edge.RISING,
            sample_mode=AcquisitionType.FINITE, samps_per_chan=10):
        """
        Sets the source of the Sample Clock, the rate of the Sample
        Clock, and the number of samples to acquire or generate.

        Args:
            rate (float): Specifies the sampling rate in samples per
                channel per second. If you use an external source for
                the Sample Clock, set this input to the maximum expected
                rate of that clock.
            source (Optional[str]): Specifies the source terminal of the
                Sample Clock. Leave this input unspecified to use the
                default onboard clock of the device.
            active_edge (Optional[artdaq.constants.Edge]): Specifies on
                which edges of Sample Clock pulses to acquire or
                generate samples.
            sample_mode (Optional[artdaq.constants.AcquisitionType]): 
                Specifies if the task acquires or generates samples
                continuously or if it acquires or generates a finite
                number of samples.
            samps_per_chan (Optional[long]): Specifies the number of
                samples to acquire or generate for each channel in the
                task if **sample_mode** is **FINITE_SAMPLES**. If
                **sample_mode** is **CONTINUOUS_SAMPLES**, DAQ uses
                this value to determine the buffer size. This function
                returns an error if the specified value is negative.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgSampClkTiming
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_double, ctypes.c_int, ctypes.c_int,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, source, rate, active_edge.value, sample_mode.value,
            samps_per_chan)
        check_for_error(error_code)