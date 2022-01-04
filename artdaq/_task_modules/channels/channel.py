from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

import artdaq
from artdaq._lib import lib_importer
from artdaq.constants import (
    ChannelType)
from artdaq.errors import (check_for_error, is_string_buffer_too_small)
from artdaq.utils import flatten_channel_string, unflatten_channel_string


class Channel(object):
    """
    Represents virtual channel or a list of virtual channels.
    """
    __slots__ = ['_handle', '_name', '__weakref__']

    def __init__(self, task_handle, virtual_or_physical_name):
        """
        Args:
            task_handle (TaskHandle): Specifies the handle of the task that
                this channel is associated with.
            virtual_or_physical_name (str): Specifies the flattened virtual or
                physical name of a channel.
        """
        self._handle = task_handle
        self._name = virtual_or_physical_name

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                'Cannot concatenate objects of type {0} and {1}'
                .format(self.__class__, other.__class__))

        if self._handle != other._handle:
            raise NotImplementedError(
                'Cannot concatenate Channel objects from different tasks.')

        name = flatten_channel_string([self.name, other.name])
        return Channel._factory(self._handle, name)

    def __contains__(self, item):
        channel_names = self.channel_names

        if isinstance(item, str):
            items = unflatten_channel_string(item)
        elif isinstance(item, Channel):
            items = item.channel_names

        return all([item in channel_names for item in items])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._handle == other._handle and
                    set(self.channel_names) == set(other.channel_names))
        return False

    def __hash__(self):
        return hash((self._handle.value, frozenset(self.channel_names)))

    def __iadd__(self, other):
        return self.__add__(other)

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

    def __repr__(self):
        return 'Channel(name={0})'.format(self.name)

    @staticmethod
    def _factory(task_handle, virtual_or_physical_name):
        """
        Implements the factory pattern for artdaq channels.

        Args:
            task_handle (TaskHandle): Specifies the handle of the task that
                this channel is associated with.
            virtual_or_physical_name (str): Specifies the flattened virtual
                or physical name of a channel.
        Returns:
            artdaq._task_modules.channels.channel.Channel:

            Indicates an object that represents the specified channel.
        """
        channel_type = ChannelType.COUNTER
        if channel_type == ChannelType.ANALOG_INPUT:
            return artdaq._task_modules.channels.AIChannel(
                task_handle, virtual_or_physical_name)
        elif channel_type == ChannelType.ANALOG_OUTPUT:
            return artdaq._task_modules.channels.AOChannel(
                task_handle, virtual_or_physical_name)
        elif channel_type == ChannelType.COUNTER:
            return artdaq._task_modules.channels.CIOChannel(
                task_handle, virtual_or_physical_name)
        elif channel_type == ChannelType.DIGITAL_IN:
            return artdaq._task_modules.channels.DIChannel(
                task_handle, virtual_or_physical_name)
        elif channel_type == ChannelType.DIGITAL_OUT:
            return artdaq._task_modules.channels.DOChannel(
                task_handle, virtual_or_physical_name)

    @property
    def name(self):
        """
        str: Specifies the name of the virtual channel this object
            represents.
        """
        if self._name:
            return self._name
        else:
            return self._all_channels_name

    @property
    def channel_names(self):
        """
        List[str]: Specifies the unflattened list of the virtual channels.
        """
        if self._name:
            return unflatten_channel_string(self._name)
        else:
            return unflatten_channel_string(self._all_channels_name)

    @property
    def _all_channels_name(self):
        """
        str: Specifies the flattened names of all the virtual channels in
            the task. such as"Dev1/ai0, Dev1/ai1, Dev1/ai2"
        """
        cfunc = lib_importer.windll.ArtDAQ_GetTaskAttribute
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

        temp_size = 256
        while True:
            val = ctypes.create_string_buffer(temp_size)

            size_or_code = cfunc(
                self._handle, 0x1273, val, temp_size)

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

    @property
    def chan_type(self):
        """
        :class:`artdaq.constants.ChannelType`: Indicates the type of
            the virtual channel.
        """
        return 0

    @property
    def line_grouping(self):
        return 0
