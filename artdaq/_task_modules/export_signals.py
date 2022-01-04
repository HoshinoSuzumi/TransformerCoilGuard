from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import lib_importer, ctypes_byte_str
from artdaq.constants import (Polarity, ExportAction, ToggleIdleState)
from artdaq.errors import check_for_error


class ExportSignals(object):
    """
    Represents the exported signal configurations for a DAQ task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def export_signal(self, signal_id, output_terminal):
        """
        Routes a control signal to the terminal you specify. The output
        terminal can reside on the device that generates the control
        signal or on a different device. You can use this function to
        share clocks and triggers among multiple tasks and devices. The
        routes this function creates are task-based routes.

        Args:
            signal_id (artdaq.constants.Signal): Is the name of the
                trigger, clock, or event to export.
            output_terminal (str): Is the destination of the exported
                signal. A DAQ terminal constant lists all terminals on
                installed devices. You can also specify a string
                containing a comma-delimited list of terminal names.
        """
        cfunc = lib_importer.windll.ArtDAQ_ExportSignal
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int,
                        ctypes_byte_str]

        error_code = cfunc(
            self._handle, signal_id.value, output_terminal)
        check_for_error(error_code)


    def export_ctrOutEvent(self, output_terminal, output_behavior=ExportAction.PULSE,
                           pulse_polarity=Polarity.ACTIVE_HIGH, toggle_idlestate=ToggleIdleState.HIGH):
        """
             Routes the counter output event to the terminal you specify.

             Args:
                 output_terminal (str): Is the destination of the exported
                     signal. A DAQ terminal constant lists all terminals on
                     installed devices. You can also specify a string
                     containing a comma-delimited list of terminal names.

                 output_behavior(artdaq.constants.ExportAction): define the output behavior is pulse or toggle.

                 pulse_polarity(artdaq.constants.Polarity): If output_behavior defined as pulse, this param defines
                 the output event is high level or low level.

                 toggle_idlestate(artdaq.constants.ToggleIdleState): If output_behavior defined as toggle,
                 this param defines the toggleIdleState is high or low.
             """
        cfunc = lib_importer.windll.ArtDAQ_ExportCtrOutEvent
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str, ctypes.c_int,
                        ctypes.c_int, ctypes.c_int]

        error_code = cfunc(
            self._handle, output_terminal, output_behavior.value, pulse_polarity.value, toggle_idlestate.value)
        check_for_error(error_code)
