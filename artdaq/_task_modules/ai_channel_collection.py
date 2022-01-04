from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import (lib_importer, ctypes_byte_str)
from artdaq._task_modules.channel_collection import ChannelCollection
from artdaq._task_modules.channels.ai_channel import AIChannel
from artdaq._task_modules.channels.channel import Channel
from artdaq.constants import (Coupling, ExcitationSource, TerminalConfiguration, VoltageUnits, ChannelType)
from artdaq.errors import check_for_error
from artdaq.utils import unflatten_channel_string


class AIChannelCollection(ChannelCollection):
    """
    Contains the collection of analog input channels for a DAQ Task.
    """
    def __init__(self, task_handle):
        super(AIChannelCollection, self).__init__(task_handle)

    def _create_chan(self, physical_channel, name_to_assign_to_channel=''):
        """
        Creates and returns an AIChannel object.

        Args:
            physical_channel (str): Specifies the names of the physical
                channels to use to create virtual channels.
            name_to_assign_to_channel (Optional[str]): Specifies a name to
                assign to the virtual channel this method creates.
        Returns:
            artdaq._task_modules.channels.ai_channel.AIChannel: 
            
            Specifies the newly created AIChannel object.
        """
        if name_to_assign_to_channel:
            num_channels = len(unflatten_channel_string(physical_channel))

            if num_channels > 1:
                name = '{0}0:{1}'.format(
                    name_to_assign_to_channel, num_channels-1)
            else:
                name = name_to_assign_to_channel
        else:
            name = physical_channel

        return AIChannel(self._handle, name)

    def add_ai_voltage_chan(
            self, physical_channel, name_to_assign_to_channel="",
            terminal_config=TerminalConfiguration.DEFAULT, min_val=-5.0,
            max_val=5.0, units=VoltageUnits.VOLTS, custom_scale_name=""):
        """
        Creates channel(s) to measure voltage. If the measurement
        requires the use of internal excitation or you need excitation
        to scale the voltage, use the AI Custom Voltage with Excitation
        instance of this function.

        Args:
            physical_channel (str): Specifies the names of the physical
                channels to use to create virtual channels. The DAQ
                physical channel constant lists all physical channels on
                devices and modules installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            terminal_config (Optional[artdaq.constants.TerminalConfiguration]):
                Specifies the input terminal configuration for the
                channel.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.VoltageUnits]): Specifies
                the units to use to return voltage measurements.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ai_channel.AIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateAIVoltageChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, ctypes.c_double,
                        ctypes.c_double, ctypes.c_int, ctypes_byte_str]

        error_code = cfunc(
            self._handle, physical_channel, name_to_assign_to_channel,
            terminal_config.value, min_val, max_val, units.value,
            custom_scale_name)
        check_for_error(error_code)
        Channel.chan_type = ChannelType.ANALOG_INPUT
        return self._create_chan(physical_channel, name_to_assign_to_channel)

    def add_ai_voltage_iepe_chan(
            self, physical_channel, name_to_assign_to_channel="",
            terminal_config=TerminalConfiguration.DEFAULT, coupling=Coupling.DC, min_val=-5.0,
            max_val=5.0,
            current_excit_source=ExcitationSource.INTERNAL,
            current_excit_val=0.004):
        """
        Creates channel(s) that use an IEPE velocity sensor to measure
        velocity.

        Args:
            physical_channel (str): Specifies the names of the physical
                channels to use to create virtual channels. The DAQ
                physical channel constant lists all physical channels on
                devices and modules installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            terminal_config (Optional[artdaq.constants.TerminalConfiguration]):
                Specifies the input terminal configuration for the
                channel.
            coupling: (Optional[artdaq.constants.Coupling])couple mode.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            current_excit_source (Optional[artdaq.constants.ExcitationSource]):
                Specifies the source of excitation.
            current_excit_val (Optional[float]): Specifies in amperes
                the amount of excitation to supply to the sensor. Refer
                to the sensor documentation to determine this value.
        Returns:
            artdaq._task_modules.channels.ai_channel.AIChannel:
            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateAIVoltageIEPEChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes.c_double]

        error_code = cfunc(
            self._handle, physical_channel, name_to_assign_to_channel,
            terminal_config.value, coupling.value, min_val, max_val, current_excit_source.value,
            current_excit_val)
        check_for_error(error_code)
        Channel.chan_type = ChannelType.ANALOG_INPUT
        return self._create_chan(physical_channel, name_to_assign_to_channel)
