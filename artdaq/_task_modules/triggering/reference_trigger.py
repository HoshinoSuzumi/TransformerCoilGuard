from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import (lib_importer, ctypes_byte_str)
from artdaq.constants import (Edge, Slope, WindowTriggerCondition1)
from artdaq.errors import check_for_error


class ReferenceTrigger(object):
    """
    Represents the reference trigger configurations for a DAQ task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def disable_ref_trig(self):
        """
        Disables reference triggering for the measurement.
        """
        cfunc = lib_importer.windll.ArtDAQ_DisablePauseTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle]

        error_code = cfunc(
            self._handle)
        check_for_error(error_code)
        
    def cfg_dig_edge_ref_trig(
            self, trigger_source, pretrigger_samples,
            trigger_edge=Edge.RISING):
        """
        Configures the task to stop the acquisition when the device
        acquires all pretrigger samples, detects a rising or falling
        edge of a digital signal, and acquires all posttrigger samples.
        When you use a Reference Trigger, the default for the read
        RelativeTo property is **first_pretrigger_sample** with a read
        Offset of 0.

        Args:
            trigger_source (str): Specifies the name of a terminal where
                there is a digital signal to use as the source of the
                trigger.
            pretrigger_samples (int): Specifies the minimum number of
                samples to acquire per channel before recognizing the
                Reference Trigger. The number of post-trigger samples
                per channel is equal to **number of samples per
                channel** in the Timing function minus
                **pretrigger_samples**.
            trigger_edge (Optional[artdaq.constants.Edge]): Specifies
                on which edge of the digital signal the Reference
                Trigger occurs.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgDigEdgeRefTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_uint]

        error_code = cfunc(
            self._handle, trigger_source, trigger_edge.value,
            pretrigger_samples)
        check_for_error(error_code)

    def cfg_anlg_edge_ref_trig(
            self, trigger_source, pretrigger_samples,
            trigger_slope=Slope.RISING, trigger_level=0.0):
        """
        Configures the task to stop the acquisition when the device
        acquires all pretrigger samples; an analog signal reaches the
        level you specify; and the device acquires all post-trigger
        samples. When you use a Reference Trigger, the default for the
        read RelativeTo property is **first_pretrigger_sample** with a
        read Offset of 0.

        Args:
            trigger_source (str): Is the name of a virtual channel or
                terminal where there is an analog signal to use as the
                source of the trigger.
            pretrigger_samples (int): Specifies the minimum number of
                samples to acquire per channel before recognizing the
                Reference Trigger. The number of post-trigger samples
                per channel is equal to **number of samples per
                channel** in the DAQ Timing function minus
                **pretrigger_samples**.
            trigger_slope (Optional[artdaq.constants.Slope]): Specifies
                on which slope of the signal the Reference Trigger
                occurs.
            trigger_level (Optional[float]): Specifies at what threshold
                to trigger. Specify this value in the units of the
                measurement or generation. Use **trigger_slope** to
                specify on which slope to trigger at this threshold.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgEdgeRefTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_double, ctypes.c_uint]

        error_code = cfunc(
            self._handle, trigger_source, trigger_slope.value, trigger_level,
            pretrigger_samples)
        check_for_error(error_code)

    def cfg_anlg_window_ref_trig(
            self, trigger_source, window_top, window_bottom,
            pretrigger_samples,
            trigger_when=WindowTriggerCondition1.ENTERING_WINDOW):
        """
        Configures the task to stop the acquisition when the device
        acquires all pretrigger samples; an analog signal enters or
        leaves a range you specify; and the device acquires all post-
        trigger samples. When you use a Reference Trigger, the default
        for the read RelativeTo property is **first_pretrigger_sample**
        with a read Offset of 0.

        Args:
            trigger_source (str): Is the name of a virtual channel or
                terminal where there is an analog signal to use as the
                source of the trigger.
            window_top (float): Is the upper limit of the window.
                Specify this value in the units of the measurement or
                generation.
            window_bottom (float): Is the lower limit of the window.
                Specify this value in the units of the measurement or
                generation.
            pretrigger_samples (int): Specifies the minimum number of
                samples to acquire per channel before recognizing the
                Reference Trigger. The number of post-trigger samples
                per channel is equal to **number of samples per
                channel** in the DAQ Timing function minus
                **pretrigger_samples**.
            trigger_when (Optional[artdaq.constants.WindowTriggerCondition1]):
                Specifies whether the Reference Trigger occurs when the
                signal enters the window or when it leaves the window.
                Use **window_bottom** and **window_top** to specify the
                limits of the window.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgWindowRefTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_double, ctypes.c_double,
                        ctypes.c_uint]

        error_code = cfunc(
            self._handle, trigger_source, trigger_when.value, window_top,
            window_bottom, pretrigger_samples)
        check_for_error(error_code)

    @property
    def dig_fltr_min_pulse_width(self):
        """
        float: Specifies in seconds the minimum pulse width the filter
            recognizes.
        """
        val = ctypes.c_double()

        cfunc = (lib_importer.windll.
                 ArtDAQ_GetRefTrigDigFltrMinPulseWidth)
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle,
                        ctypes.POINTER(ctypes.c_double)]

        error_code = cfunc(
            self._handle, ctypes.byref(val))
        check_for_error(error_code)

        return val.value

    @dig_fltr_min_pulse_width.setter
    def dig_fltr_min_pulse_width(self, val):
        cfunc = (lib_importer.windll.
                 ArtDAQ_SetRefTrigDigFltrMinPulseWidth)
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_double]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)
