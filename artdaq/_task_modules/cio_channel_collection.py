from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

from artdaq._lib import lib_importer, ctypes_byte_str, c_bool32
from artdaq._task_modules.channel_collection import ChannelCollection
from artdaq._task_modules.channels.channel import Channel
from artdaq._task_modules.channels.cio_channel import CIOChannel
from artdaq.constants import (
    AngleUnits, CountDirection, CounterFrequencyMethod,
    Edge, EncoderType, EncoderZIndexPhase, LengthUnits, UsageTypeCI,
    FrequencyUnits, Level, TimeUnits, UsageTypeCO, ChannelType)
from artdaq.errors import check_for_error
from artdaq.utils import unflatten_channel_string


class CIOChannelCollection(ChannelCollection):
    """
    Contains the collection of counter input channels for a DAQ Task.
    """
    def __init__(self, task_handle):
        super(CIOChannelCollection, self).__init__(task_handle)

    def _create_chan(self, counter, name_to_assign_to_channel=''):
        """
        Creates and returns a CIChannel object.

        Args:
            counter (str): Specifies the names of the counters to use to 
                create virtual channels.
            name_to_assign_to_channel (Optional[str]): Specifies a name to 
                assign to the virtual channel this method creates.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel: 
            
            Specifies the newly created CIChannel object.
        """
        if name_to_assign_to_channel:
            num_counters = len(unflatten_channel_string(counter))

            if num_counters > 1:
                name = '{0}0:{1}'.format(
                    name_to_assign_to_channel, num_counters-1)
            else:
                name = name_to_assign_to_channel
        else:
            name = counter

        Channel.chan_type = ChannelType.COUNTER
        return CIOChannel(self._handle, name)

    def add_ci_freq_chan(
            self, counter, name_to_assign_to_channel="", min_val=0.1,
            max_val=2000000.0, units=FrequencyUnits.HZ, edge=Edge.RISING,
            meas_method=CounterFrequencyMethod.LOW_FREQUENCY_1_COUNTER,
            meas_time=0.001, divisor=4, custom_scale_name=""):
        """
        Creates a channel to measure the frequency of a digital signal.
        With the exception of devices that support multi-counter tasks,
        you can create only one counter input channel at a time with
        this function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.FrequencyUnits]):
                Specifies the units to use to return frequency
                measurements.
            edge (Optional[artdaq.constants.Edge]): Specifies between
                which edges to measure the frequency or period of the
                signal.
            meas_method (Optional[artdaq.constants.CounterFrequencyMethod]):
                Specifies the method to use to calculate the period or
                frequency of the signal.
            meas_time (Optional[float]): Is the length of time in
                seconds to measure the frequency or period of the signal
                if **meas_method** is **HIGH_FREQUENCYWITH_2_COUNTERS**.
                Leave this input unspecified if **meas_method** is not
                **HIGH_FREQUENCYWITH_2_COUNTERS**.
            divisor (Optional[int]): Is the value by which to divide the
                input signal when **meas_method** is
                **LARGE_RANGEWITH_2_COUNTERS**. Leave this input
                unspecified if **meas_method** is not
                **LARGE_RANGEWITH_2_COUNTERS**.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIFreqChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_uint, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value, edge.value, meas_method.value, meas_time,
            divisor, custom_scale_name)
        check_for_error(error_code)

        CIOChannel.ci_meas_type = UsageTypeCI.FREQUENCY
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_period_chan(
            self, counter, name_to_assign_to_channel="", min_val=0.000001,
            max_val=0.1, units=TimeUnits.SECONDS, edge=Edge.RISING,
            meas_method=CounterFrequencyMethod.LOW_FREQUENCY_1_COUNTER,
            meas_time=0.001, divisor=4, custom_scale_name=""):
        """
        Creates a channel to measure the period of a digital signal.
        With the exception of devices that support multi-counter tasks,
        you can create only one counter input channel at a time with
        this function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return time or period measurements.
            edge (Optional[artdaq.constants.Edge]): Specifies between
                which edges to measure the frequency or period of the
                signal.
            meas_method (Optional[artdaq.constants.CounterFrequencyMethod]):
                Specifies the method to use to calculate the period or
                frequency of the signal.
            meas_time (Optional[float]): Is the length of time in
                seconds to measure the frequency or period of the signal
                if **meas_method** is **HIGH_FREQUENCYWITH_2_COUNTERS**.
                Leave this input unspecified if **meas_method** is not
                **HIGH_FREQUENCYWITH_2_COUNTERS**.
            divisor (Optional[int]): Is the value by which to divide the
                input signal when **meas_method** is
                **LARGE_RANGEWITH_2_COUNTERS**. Leave this input
                unspecified if **meas_method** is not
                **LARGE_RANGEWITH_2_COUNTERS**.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIPeriodChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_uint, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value, edge.value, meas_method.value, meas_time,
            divisor, custom_scale_name)
        check_for_error(error_code)

        CIOChannel.ci_meas_type = UsageTypeCI.PERIOD
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_count_edges_chan(
            self, counter, name_to_assign_to_channel="", edge=Edge.RISING,
            initial_count=0, count_direction=CountDirection.COUNT_UP):
        """
        Creates a channel to count the number of rising or falling edges
        of a digital signal. With the exception of devices that support
        multi-counter tasks, you can create only one counter input
        channel at a time with this function because a task can contain
        only one counter input channel. To read from multiple counters
        simultaneously, use a separate task for each counter. Connect
        the input signal to the default input terminal of the counter
        unless you select a different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            edge (Optional[artdaq.constants.Edge]): Specifies on which
                edges of the input signal to increment or decrement the
                count.
            initial_count (Optional[int]): Is the value from which to
                start counting.
            count_direction (Optional[artdaq.constants.CountDirection]):
                Specifies whether to increment or decrement the counter
                on each edge.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCICountEdgesChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, ctypes.c_uint,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, edge.value,
            initial_count, count_direction.value)
        check_for_error(error_code)

        CIOChannel.ci_meas_type = UsageTypeCI.COUNT_EDGES
        Channel.chan_type = ChannelType.COUNTER
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_pulse_chan_time(
            self, counter, name_to_assign_to_channel="", min_val=0.1,
            max_val=1000, units=TimeUnits.SECONDS):
        """
        Creates a channel to measure pulse specifications, returning the
        measurements as pairs of high time and low time. With the
        exception of devices that support multi-counter tasks, you can
        create only one counter input channel at a time with this
        function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return pulse specifications in terms of
                high time and low time.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.DAQCreateCIPulseChanTime
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_TIME
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_pulse_width_chan(
            self, counter, name_to_assign_to_channel="", min_val=0.000001,
            max_val=0.1, units=TimeUnits.SECONDS, starting_edge=Edge.RISING,
            custom_scale_name=""):
        """
        Creates a channel to measure the width of a digital pulse.
        **starting_edge** determines whether to measure a high pulse or
        low pulse. With the exception of devices that support multi-
        counter tasks, you can create only one counter input channel at
        a time with this function because a task can contain only one
        counter input channel. To read from multiple counters
        simultaneously, use a separate task for each counter. Connect
        the input signal to the default input terminal of the counter
        unless you select a different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return time or period measurements.
            starting_edge (Optional[artdaq.constants.Edge]): Specifies
                on which edge to begin measuring pulse width.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIPulseWidthChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes.c_int, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value, starting_edge.value, custom_scale_name)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_WIDTH_DIGITAL
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_semi_period_chan(
            self, counter, name_to_assign_to_channel="", min_val=0.000001,
            max_val=10, units=TimeUnits.SECONDS, custom_scale_name=""):
        """
        Creates a channel to measure the time between state transitions
        of a digital signal. With the exception of devices that support
        multi-counter tasks, you can create only one counter input
        channel at a time with this function because a task can contain
        only one counter input channel. To read from multiple counters
        simultaneously, use a separate task for each counter. Connect
        the input signal to the default input terminal of the counter
        unless you select a different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return time or period measurements.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCISemiPeriodChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value, custom_scale_name)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_WIDTH_DIGITAL_SEMI_PERIOD
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_two_edge_sep_chan(
            self, counter, name_to_assign_to_channel="", min_val=0.000001,
            max_val=10.0, units=TimeUnits.SECONDS, first_edge=Edge.RISING,
            second_edge=Edge.FALLING, custom_scale_name=""):
        """
        Creates a channel that measures the amount of time between the
        rising or falling edge of one digital signal and the rising or
        falling edge of another digital signal. With the exception of
        devices that support multi-counter tasks, you can create only
        one counter input channel at a time with this function because a
        task can contain only one counter input channel. To read from
        multiple counters simultaneously, use a separate task for each
        counter. Connect the input signals to the default input
        terminals of the counter unless you select different input
        terminals.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return time or period measurements.
            first_edge (Optional[artdaq.constants.Edge]): Specifies on
                which edge of the first signal to start each
                measurement.
            second_edge (Optional[artdaq.constants.Edge]): Specifies on
                which edge of the second signal to stop each
                measurement.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCITwoEdgeSepChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int, ctypes.c_int, ctypes.c_int,
                        ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value, first_edge.value, second_edge.value,
            custom_scale_name)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_WIDTH_DIGITAL_TWO_EDGE_SEPARATION
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_pulse_chan_freq(
            self, counter, name_to_assign_to_channel="", min_val=0.1,
            max_val=200000, units=FrequencyUnits.HZ):
        """
        Creates a channel to measure pulse specifications, returning the
        measurements as pairs of frequency and duty cycle. With the
        exception of devices that support multi-counter tasks, you can
        create only one counter input channel at a time with this
        function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.FrequencyUnits]):
                Specifies the units to use to return pulse
                specifications in terms of frequency.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIPulseChanFreq
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_FREQ
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_pulse_chan_time(
            self, counter, name_to_assign_to_channel="", min_val=0.000001,
            max_val=0.001, units=TimeUnits.SECONDS):
        """
        Creates a channel to measure pulse specifications, returning the
        measurements as pairs of high time and low time. With the
        exception of devices that support multi-counter tasks, you can
        create only one counter input channel at a time with this
        function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units to use to return pulse specifications in terms of
                high time and low time.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIPulseChanTime
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_double, ctypes.c_double,
                        ctypes.c_int]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, min_val,
            max_val, units.value)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_TIME
        Channel.chan_type = ChannelType.COUNTER
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_pulse_chan_ticks(
            self, counter, name_to_assign_to_channel="",
            source_terminal="100MHzTimebase", min_val=2, max_val=2000000):
        """
        Creates a channel to measure pulse specifications, returning the
        measurements as pairs of high ticks and low ticks. With the
        exception of devices that support multi-counter tasks, you can
        create only one counter input channel at a time with this
        function because a task can contain only one counter input
        channel. To read from multiple counters simultaneously, use a
        separate task for each counter. Connect the input signal to the
        default input terminal of the counter unless you select a
        different input terminal.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            source_terminal (Optional[str]): Is the terminal to which
                you connect a signal to use as the source of ticks. A
                DAQ terminal constant lists all terminals available on
                devices installed in the system. You also can specify a
                source terminal by specifying a string that contains a
                terminal name. If you specify OnboardClock, or do not
                specify any terminal, ArtDAQ selects the fastest
                onboard timebase available on the device.
            min_val (Optional[float]): Specifies in **units** the
                minimum value you expect to measure.
            max_val (Optional[float]): Specifies in **units** the
                maximum value you expect to measure.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIPulseChanTicks
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes_byte_str, ctypes.c_double,
                        ctypes.c_double]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, source_terminal,
            min_val, max_val)
        check_for_error(error_code)

        CIOChannel.ci_meas_type = UsageTypeCI.PULSE_TICKS

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_lin_encoder_chan(
            self, counter, name_to_assign_to_channel="",
            decoding_type=EncoderType.X_4, zidx_enable=False, zidx_val=0,
            zidx_phase=EncoderZIndexPhase.AHIGH_BHIGH,
            units=LengthUnits.METERS, dist_per_pulse=0.001, initial_pos=0.0,
            custom_scale_name=""):
        """
        Creates a channel that uses a linear encoder to measure linear
        position. With the exception of devices that support multi-
        counter tasks, you can create only one counter input channel at
        a time with this function because a task can contain only one
        counter input channel. To read from multiple counters
        simultaneously, use a separate task for each counter. Connect
        the input signals to the default input terminals of the counter
        unless you select different input terminals.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            decoding_type (Optional[artdaq.constants.EncoderType]):
                Specifies how to count and interpret the pulses the
                encoder generates on signal A and signal B. **X_1**,
                **X_2**, and **X_4** are valid for quadrature encoders
                only. **TWO_PULSE_COUNTING** is valid only for two-pulse
                encoders.
            zidx_enable (Optional[bool]): Specifies whether to use Z
                indexing for the channel.
            zidx_val (Optional[float]): Specifies in **units** the value
                to which to reset the measurement when signal Z is high
                and signal A and signal B are at the states you specify
                with **zidx_phase**.
            zidx_phase (Optional[artdaq.constants.EncoderZIndexPhase]):
                Specifies the states at which signal A and signal B must
                be while signal Z is high for ArtDAQ to reset the
                measurement. If signal Z is never high while signal A
                and signal B are high, for example, you must choose a
                phase other than **A_HIGH_B_HIGH**.
            units (Optional[artdaq.constants.LengthUnits]): Specifies
                the units to use to return linear position measurements
                from the channel.
            dist_per_pulse (Optional[float]): Is the distance to measure
                for each pulse the encoder generates on signal A or
                signal B. This value is in the units you specify with
                the **units** input.
            initial_pos (Optional[float]): Is the position of the
                encoder when you begin the measurement. This value is in
                the units you specify with the **units** input.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCILinEncoderChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, c_bool32,
                        ctypes.c_double, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_double, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel,
            decoding_type.value, zidx_enable, zidx_val, zidx_phase.value,
            units.value, dist_per_pulse, initial_pos, custom_scale_name)
        check_for_error(error_code)

        CIOChannel.ci_meas_type = UsageTypeCI.POSITION_LINEAR_ENCODER
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_ci_ang_encoder_chan(
            self, counter, name_to_assign_to_channel="",
            decoding_type=EncoderType.X_4, zidx_enable=False, zidx_val=0,
            zidx_phase=EncoderZIndexPhase.AHIGH_BHIGH,
            units=AngleUnits.DEGREES, pulses_per_rev=24, initial_angle=0.0,
            custom_scale_name=""):
        """
        Creates a channel that uses an angular encoder to measure
        angular position. With the exception of devices that support
        multi-counter tasks, you can create only one counter input
        channel at a time with this function because a task can contain
        only one counter input channel. To read from multiple counters
        simultaneously, use a separate task for each counter. Connect
        the input signals to the default input terminals of the counter
        unless you select different input terminals.

        Args:
            counter (str): Specifies the name of the counter to use to
                create the virtual channel. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            decoding_type (Optional[artdaq.constants.EncoderType]):
                Specifies how to count and interpret the pulses the
                encoder generates on signal A and signal B. **X_1**,
                **X_2**, and **X_4** are valid for quadrature encoders
                only. **TWO_PULSE_COUNTING** is valid only for two-pulse
                encoders.
            zidx_enable (Optional[bool]): Specifies whether to use Z
                indexing for the channel.
            zidx_val (Optional[float]): Specifies in **units** the value
                to which to reset the measurement when signal Z is high
                and signal A and signal B are at the states you specify
                with **zidx_phase**.
            zidx_phase (Optional[artdaq.constants.EncoderZIndexPhase]):
                Specifies the states at which signal A and signal B must
                be while signal Z is high for ArtDAQ to reset the
                measurement. If signal Z is never high while signal A
                and signal B are high, for example, you must choose a
                phase other than **A_HIGH_B_HIGH**.
            units (Optional[artdaq.constants.AngleUnits]): Specifies
                the units to use to return angular position measurements
                from the channel.
            pulses_per_rev (Optional[int]): Is the number of pulses the
                encoder generates per revolution. This value is the
                number of pulses on either signal A or signal B, not the
                total number of pulses on both signal A and signal B.
            initial_angle (Optional[float]): Is the starting angle of
                the encoder. This value is in the units you specify with
                the **units** input.
            custom_scale_name (Optional[str]): Specifies the name of a
                custom scale for the channel. If you want the channel to
                use a custom scale, specify the name of the custom scale
                to this input and set **units** to
                **FROM_CUSTOM_SCALE**.
        Returns:
            artdaq._task_modules.channels.ci_channel.CIChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCIAngEncoderChan
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, c_bool32,
                        ctypes.c_double, ctypes.c_int, ctypes.c_int,
                        ctypes.c_uint, ctypes.c_double, ctypes_byte_str]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel,
            decoding_type.value, zidx_enable, zidx_val, zidx_phase.value,
            units.value, pulses_per_rev, initial_angle, custom_scale_name)
        check_for_error(error_code)
        CIOChannel.ci_meas_type = UsageTypeCI.POSITION_ANGULAR_ENCODER
        Channel.chan_type = ChannelType.COUNTER
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_co_pulse_chan_freq(
            self, counter, name_to_assign_to_channel="",
            units=FrequencyUnits.HZ, idle_state=Level.LOW, initial_delay=0.0,
            freq=1.0, duty_cycle=0.5):
        """
        Creates channel(s) to generate digital pulses that **freq** and
        **duty_cycle** define. The pulses appear on the default output
        terminal of the counter unless you select a different output
        terminal.

        Args:
            counter (str): Specifies the names of the counters to use to
                create the virtual channels. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            units (Optional[artdaq.constants.FrequencyUnits]):
                Specifies the units in which to define pulse frequency.
            idle_state (Optional[artdaq.constants.Level]): Specifies
                the resting state of the output terminal.
            initial_delay (Optional[float]): Is the amount of time in
                seconds to wait before generating the first pulse.
            freq (Optional[float]): Specifies at what frequency to
                generate pulses.
            duty_cycle (Optional[float]): Is the width of the pulse
                divided by the pulse period. ArtDAQ uses this ratio
                combined with frequency to determine pulse width and the
                interval between pulses.
        Returns:
            artdaq._task_modules.channels.co_channel.COChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCOPulseChanFreq
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_double, ctypes.c_double]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, units.value,
            idle_state.value, initial_delay, freq, duty_cycle)
        check_for_error(error_code)
        CIOChannel.co_output_type = UsageTypeCO.PULSE_FREQUENCY
        Channel.chan_type = ChannelType.COUNTER
        return self._create_chan(counter, name_to_assign_to_channel)

    def add_co_pulse_chan_ticks(
            self, counter, source_terminal, name_to_assign_to_channel="",
            idle_state=Level.LOW, initial_delay=0, low_ticks=100,
            high_ticks=100):
        """
        Creates channel(s) to generate digital pulses defined by the
        number of timebase ticks that the pulse is at a high state and
        the number of timebase ticks that the pulse is at a low state.
        The pulses appear on the default output terminal of the counter
        unless you select a different output terminal.

        Args:
            counter (str): Specifies the names of the counters to use to
                create the virtual channels. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            source_terminal (str): Is the terminal to which you connect
                an external timebase. A DAQ terminal constant lists
                all terminals available on devices installed in the
                system. You also can specify a source terminal by
                specifying a string that contains a terminal name.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            idle_state (Optional[artdaq.constants.Level]): Specifies
                the resting state of the output terminal.
            initial_delay (Optional[int]): Is the number of timebase
                ticks to wait before generating the first pulse.
            low_ticks (Optional[int]): Is the number of ticks the pulse
                is low.
            high_ticks (Optional[int]): Is the number of ticks the pulse
                is high.
        Returns:
            artdaq._task_modules.channels.co_channel.COChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCOPulseChanTicks
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes_byte_str, ctypes.c_int,
                        ctypes.c_int, ctypes.c_int, ctypes.c_int]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, source_terminal,
            idle_state.value, initial_delay, low_ticks, high_ticks)
        check_for_error(error_code)
        CIOChannel.co_output_type = UsageTypeCO.PULSE_TICKS
        Channel.chan_type = ChannelType.COUNTER

        return self._create_chan(counter, name_to_assign_to_channel)

    def add_co_pulse_chan_time(
            self, counter, name_to_assign_to_channel="",
            units=TimeUnits.SECONDS, idle_state=Level.LOW, initial_delay=0.0,
            low_time=0.01, high_time=0.01):
        """
        Creates channel(s) to generate digital pulses defined by the
        amount of time the pulse is at a high state and the amount of
        time the pulse is at a low state. The pulses appear on the
        default output terminal of the counter unless you select a
        different output terminal.

        Args:
            counter (str): Specifies the names of the counters to use to
                create the virtual channels. The DAQ physical channel
                constant lists all physical channels, including
                counters, for devices installed in the system.
            name_to_assign_to_channel (Optional[str]): Specifies a name
                to assign to the virtual channel this function creates.
                If you do not specify a value for this input, ArtDAQ
                uses the physical channel name as the virtual channel
                name.
            units (Optional[artdaq.constants.TimeUnits]): Specifies the
                units in which to define pulse high and low time.
            idle_state (Optional[artdaq.constants.Level]): Specifies
                the resting state of the output terminal.
            initial_delay (Optional[float]): Is the amount of time in
                seconds to wait before generating the first pulse.
            low_time (Optional[float]): Is the amount of time the pulse
                is low.
            high_time (Optional[float]): Is the amount of time the pulse
                is high.
        Returns:
            artdaq._task_modules.channels.co_channel.COChannel:

            Indicates the newly created channel object.
        """
        cfunc = lib_importer.windll.ArtDAQ_CreateCOPulseChanTime
        if cfunc.argtypes is None:
            with cfunc.arglock:
                if cfunc.argtypes is None:
                    cfunc.argtypes = [
                        lib_importer.task_handle, ctypes_byte_str,
                        ctypes_byte_str, ctypes.c_int, ctypes.c_int,
                        ctypes.c_double, ctypes.c_double, ctypes.c_double]

        error_code = cfunc(
            self._handle, counter, name_to_assign_to_channel, units.value,
            idle_state.value, initial_delay, low_time, high_time)
        check_for_error(error_code)
        CIOChannel.co_output_type = UsageTypeCO.PULSE_TIME
        Channel.chan_type = ChannelType.COUNTER
        return self._create_chan(counter, name_to_assign_to_channel)
