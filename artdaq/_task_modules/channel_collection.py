from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections.abc import Sequence

import six

from artdaq._task_modules.channels.channel import Channel
from artdaq.errors import DaqError
from artdaq.utils import unflatten_channel_string, flatten_channel_string


class ChannelCollection(Sequence):
    """
    Contains the collection of channels for a DAQ Task.
    
    This class defines methods that implements a container object.
    """
    def __init__(self, task_handle):
        self._handle = task_handle

    def __contains__(self, item):
        channel_names = self.channel_names
        if isinstance(item, six.string_types):
            items = unflatten_channel_string(item)
        elif isinstance(item, Channel):
            items = item.channel_names
        return all([item in channel_names for item in items])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._handle == other._handle
        return False

    def __getitem__(self, index):
        """
        Indexes a subset of virtual channels on this channel collection.

        Args:
            index: The value of the index. The following index types are
                supported:
                - str: Name of the virtual channel. You also can specify a
                    string that contains a list or range of names to this
                    input. If you have a list of names, use the DAQ
                    Flatten Channel String function to convert the list to a
                    string.
                - int: Index/position of the virtual channel in the collection.
                - slice: Range of the indexes/positions of virtual channels in
                    the collection.
        Returns:
            artdaq._task_modules.channels.channel.Channel: 
            
            Indicates a channel object representing the subset of virtual
            channels indexed.
        """
        if isinstance(index, six.integer_types):
            channel_names = self.channel_names[index]
        elif isinstance(index, slice):
            channel_names = flatten_channel_string(self.channel_names[index])
        elif isinstance(index, six.string_types):
            channel_names = index
        else:
            raise DaqError(
                'Invalid index type "{0}" used to access channels.'
                .format(type(index)), DaqError.UNKNOWN.value)

    def __hash__(self):
        return hash(self._handle.value)

    def __iter__(self):
        for channel_name in self.channel_names:
            yield Channel._factory(self._handle, channel_name)

    def __len__(self):
        return len(self.channel_names)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reversed__(self):
        channel_names = self.channel_names
        channel_names.reverse()

        for channel_name in channel_names:
            yield Channel._factory(self._handle, channel_name)

    @property
    def all(self):
        """
        :class:`artdaq._task_modules.channels.channel.Channel`:
            Specifies a channel object that represents the entire list of 
            virtual channels on this channel collection.
        """
        # Passing a blank string means all channels.
        return Channel._factory(self._handle, '')
    