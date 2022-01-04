from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from artdaq._task_modules.triggering.pause_trigger import PauseTrigger
from artdaq._task_modules.triggering.reference_trigger import ReferenceTrigger
from artdaq._task_modules.triggering.start_trigger import StartTrigger


class Triggers(object):
    """
    Represents the trigger configurations for a DAQmx task.
    """
    def __init__(self, task_handle):
        self._handle = task_handle
        self._pause_trigger = PauseTrigger(self._handle)
        self._reference_trigger = ReferenceTrigger(self._handle)
        self._start_trigger = StartTrigger(self._handle)

    @property
    def pause_trigger(self):
        """
        :class:`artdaq._task_modules.triggering.pause_trigger.PauseTrigger`:
            Gets the pause trigger configurations for the task.
        """
        return self._pause_trigger

    @property
    def reference_trigger(self):
        """
        :class:`artdaq._task_modules.triggering.reference_trigger.ReferenceTrigger`:
            Gets the reference trigger configurations for the task.
        """
        return self._reference_trigger

    @property
    def start_trigger(self):
        """
        :class:`artdaq._task_modules.triggering.start_trigger.StartTrigger`:
            Gets the start trigger configurations for the task.
        """
        return self._start_trigger
