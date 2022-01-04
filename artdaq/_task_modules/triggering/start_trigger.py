from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import (lib_importer, ctypes_byte_str, c_bool32)
from artdaq.constants import (Edge, Slope, WindowTriggerCondition1, DigitalWidthUnits)
from artdaq.errors import check_for_error


class StartTrigger(object):
    """
    Represents the start trigger configurations for a DAQ task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def disable_start_trig(self):
        """
        Configures the task to start acquiring or generating samples
        immediately upon starting the task.
        """
        cfunc = lib_importer.windll.ArtDAQ_DisableStartTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle]

        error_code = cfunc(
            self._handle)
        check_for_error(error_code)

    def cfg_dig_edge_start_trig(
            self, trigger_source, trigger_edge=Edge.RISING):
        """
        Configures the task to start acquiring or generating samples on
        a rising or falling edge of a digital signal.

        Args:
            trigger_source (str): Specifies the name of a terminal where
                there is a digital signal to use as the source of the
                trigger.
            trigger_edge (Optional[artdaq.constants.Edge]): Specifies
                on which edge of the digital signal to start acquiring
                or generating samples.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgDigEdgeStartTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, trigger_source, trigger_edge.value)
        check_for_error(error_code)

    def cfg_anlg_edge_start_trig(
            self, trigger_source="", trigger_slope=Slope.RISING,
            trigger_level=0.0):
        """
        Configures the task to start acquiring or generating samples
        when an analog signal crosses the level you specify.

        Args:
            trigger_source (Optional[str]): Is the name of a virtual
                channel or terminal where there is an analog signal to
                use as the source of the trigger.
            trigger_slope (Optional[artdaq.constants.Slope]): Specifies
                on which slope of the signal to start acquiring or
                generating samples when the signal crosses
                **trigger_level**.
            trigger_level (Optional[float]): Specifies at what threshold
                to start acquiring or generating samples. Specify this
                value in the units of the measurement or generation. Use
                **trigger_slope** to specify on which slope to trigger
                at this threshold.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgEdgeStartTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_double]

        error_code = cfunc(
            self._handle, trigger_source, trigger_slope.value, trigger_level)
        check_for_error(error_code)

    def cfg_anlg_window_start_trig(
            self, window_top, window_bottom, trigger_source="",
            trigger_when=WindowTriggerCondition1.ENTERING_WINDOW):
        """
        Configures the task to start acquiring or generating samples
        when an analog signal enters or leaves a range you specify.

        Args:
            window_top (float): Is the upper limit of the window.
                Specify this value in the units of the measurement or
                generation.
            window_bottom (float): Is the lower limit of the window.
                Specify this value in the units of the measurement or
                generation.
            trigger_source (Optional[str]): Is the name of a virtual
                channel or terminal where there is an analog signal to
                use as the source of the trigger.
            trigger_when (Optional[artdaq.constants.WindowTriggerCondition1]):
                Specifies whether the task starts measuring or
                generating samples when the signal enters the window or
                when it leaves the window. Use **window_bottom** and
                **window_top** to specify the limits of the window.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgWindowStartTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_double, ctypes.c_double]

        error_code = cfunc(
            self._handle, trigger_source, trigger_when.value, window_top,
            window_bottom)
        check_for_error(error_code)

    @property
    def delay(self):
        """
        float: Specifies an amount of time to wait after the Start
            Trigger is received before acquiring or generating the first
            sample. This value is in the units you specify with
            **delay_units**.
        """
        val = ctypes.c_double()

        cfunc = lib_importer.windll.ArtDAQ_GetStartTrigDelay
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

    @delay.setter
    def delay(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetStartTrigDelay
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_double]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    @property
    def delay_units(self):
        """
        :class:`artdaq.constants.DigitalWidthUnits`: Specifies the
            units of **delay**.
        """
        val = ctypes.c_int()

        cfunc = lib_importer.windll.ArtDAQ_GetStartTrigDelayUnits
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.POINTER(ctypes.c_int)]

        error_code = cfunc(
            self._handle, ctypes.byref(val))
        check_for_error(error_code)

        return DigitalWidthUnits(val.value)

    @delay_units.setter
    def delay_units(self, val):
        val = val.value
        cfunc = lib_importer.windll.ArtDAQ_SetStartTrigDelayUnits
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    @property
    def dig_fltr_min_pulse_width(self):
        """
        float: Specifies in seconds the minimum pulse width the filter
            recognizes.
        """
        val = ctypes.c_double()

        cfunc = (lib_importer.windll.
                 ArtDAQ_GetStartTrigDigFltrMinPulseWidth)
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
                 ArtDAQ_SetStartTrigDigFltrMinPulseWidth)
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_double]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)

    @property
    def retriggerable(self):
        """
        bool: Specifies whether a finite task resets and waits for
            another Start Trigger after the task completes. When you set
            this property to True, the device performs a finite
            acquisition or generation each time the Start Trigger occurs
            until the task stops. The device ignores a trigger if it is
            in the process of acquiring or generating signals.
        """
        val = c_bool32()

        cfunc = lib_importer.windll.ArtDAQ_GetStartTrigRetriggerable
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.POINTER(c_bool32)]

        error_code = cfunc(
            self._handle, ctypes.byref(val))
        check_for_error(error_code)

        return val.value

    @retriggerable.setter
    def retriggerable(self, val):
        cfunc = lib_importer.windll.ArtDAQ_SetStartTrigRetriggerable
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, c_bool32]

        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)
