from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import (lib_importer, ctypes_byte_str)
from artdaq.constants import (ActiveLevel, Level, WindowTriggerCondition2)
from artdaq.errors import (check_for_error)


class PauseTrigger(object):
    """
    Represents the pause trigger configurations for a DAQ task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def disable_pause_trig(self):
        """
        Configures the task to start acquiring or generating samples
        immediately upon starting the task.
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

    def cfg_dig_lvl_pause_trig(
            self, trigger_source, trigger_when=Level.HIGH):
        """
        Configures the task to pause acquiring or generating samples on
        a high or low digital level.

        Args:
            trigger_source (str): Specifies the name of a terminal where
                there is a digital signal to use as the source of the
                trigger.
            trigger_when (Optional[artdaq.constants.Level]): Specifies
                on which level of the digital signal to pause acquiring
                or generating samples.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgDigLvlPauseTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, trigger_source, trigger_when.value)
        check_for_error(error_code)

    def cfg_anlg_lvl_pause_trig(
            self, trigger_source, trigger_when=ActiveLevel.ABOVE, trigger_level=0.0):
        """
        Configures the task to pause acquiring or generating samples
        while the signal is above or below the threshold.

        Args:
            trigger_source (str): Specifies the name of a terminal where
                there is a anlg signal to use as the source of the
                trigger.
            trigger_when (Optional[artdaq.constants.ActiveLevel]): Specifies
                on above or below of the signal threshold to pause acquiring
                or generating samples.
            trigger_level: the signal threshold
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgLvlPauseTrig
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes.c_int, ctypes.c_double]

        error_code = cfunc(
            self._handle, trigger_source, trigger_when.value, trigger_level)
        check_for_error(error_code)

    def cfg_anlg_window_pause_trig(
            self, window_top, window_bottom, trigger_source="",
            trigger_when=WindowTriggerCondition2.INSIDE_WINDOW):
        """
        Configures the task to pause acquiring or generating samples
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
            trigger_when (Optional[artdaq.constants.WindowTriggerCondition2]):
                Specifies whether the task pauses measuring or
                generating samples when the signal inside the window or
                when it leaves the window. Use **window_bottom** and
                **window_top** to specify the limits of the window.
        """
        cfunc = lib_importer.windll.ArtDAQ_CfgAnlgWindowPauseTrig
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
    def dig_fltr_min_pulse_width(self):
        """
        float: Specifies in seconds the minimum pulse width the filter
            recognizes.
        """
        val = ctypes.c_double()

        cfunc = (lib_importer.windll.
                 ArtDAQ_GetPauseTrigDigFltrMinPulseWidth)
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
        cfunc = lib_importer.windll.ArtDAQ_SetPauseTrigDigFltrMinPulseWidth
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [lib_importer.task_handle, ctypes.c_double]
        error_code = cfunc(
            self._handle, val)
        check_for_error(error_code)