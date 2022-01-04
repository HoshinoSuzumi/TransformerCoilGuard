from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from artdaq._task_modules.channels.channel import Channel


class DIChannel(Channel):
    """
    Represents one or more digital input virtual channels and their properties.
    """
    __slots__ = []

    def __repr__(self):
        return 'DIChannel(name={0})'.format(self._name)
