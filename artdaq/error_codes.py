from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from enum import Enum

__all__ = ['Errors', 'Warnings']


class Errors(Enum):
    SERVICES_CAN_NOT_CONNECT = -229779
    SEND_SERVICES_DATA = -229778
    RECEIVE_SERVICES_DATA = -229776
    SERVICES_RESPONSE_ERROR = -229775

    PAL_COMMUNICATIONS_FAULT = -50401
    PAL_DEVICE_INITIALIZATION_FAULT = -50303
    PAL_DEVICE_NOT_SUPPORTED = -50302
    PAL_DEVICE_UNKNOWN = -50301
    PAL_MEMORY_CONFIGURATION_FAULT = -50350
    PAL_RESOURCE_RESERVED = -50103
    PAL_FUNCTION_NOT_FOUND = -50255

    BUFFER_TOO_SMALL_FOR_STRING = -200228
    READ_BUFFER_TOO_SMALL = -200229
    NULL_PTR = -200604
    DUPLICATE_TASK = -200089
    INVALID_TASK_NAME = -201340
    INVALID_DEVICE_NAME = -201339
    DEVICE_NOT_EXIST = -200220

    INVALID_PHYS_CHANNEL_STRING = -201237
    PHYSICAL_CHANNEL_DOES_NOT_EXIT = -200170
    DEV_ALREADY_IN_TASK = -200481
    CHANNEL_ALREADY_IN_TASK = -200489
    CHANNEL_NOT_IN_TASK = -200486
    DEV_NOT_IN_TASK = -200482
    INVALID_TASK = -200088
    INVALID_CHANNEL = -200087
    INVALID_SYNTAX_FOR_PHYSICAL_CHANNEL_RANGE = -200086
    MULTI_CHANNEL_TYPES_IN_TASK = -200559
    MULTI_DEVS_IN_TASK = -200558
    PHYS_CHANNEL_DEV_NOT_IN_TASK = -200648
    REF_AND_PAUSE_TRIG_CONFIGURED = -200628
    ACTIVE_PHYS_CHANNEL_TOO_MANY_LINES_SPECD_WHEN_GETTING_PRPTY = -200625
    ACTIVE_DEV_NOT_SUPPORTED_WITH_MULTI_DEV_TASK = -201207
    REAL_DEV_AND_SIM_DEV_NOT_SUPPORTED_IN_SAME_TASK = -201206
    DEVS_WITHOUT_SYNC_STRATEGIES = -201426
    DEV_CANNOT_BE_ACCESSED = -201003
    SAMPLE_RATE_NUM_CHANNELS_CONVERT_PERIOD_COMBO = -200081
    INVALID_ATTRIBUTE_VALUE = -200077
    CAN_NOT_PERFORM_OP_WHILE_TASK_RUNNING = -200479
    CAN_NOT_PERFORM_OP_WHEN_NO_CHANS_IN_TASK = -200478
    CAN_NOT_PERFORM_OP_WHEN_NO_DEV_IN_TASK = -200477
    ERROR_OPERATION_TIMED_OUT = -200474
    CAN_NOT_SET_PROPERTY_WHEN_TASK_RUNNING = -200557
    WHITE_FALIS_BUFFER_SIZE_AUTO_CONFIGURED = -200547
    CAN_NOT_READ_WHEN_AUTO_START_FALSE_AND_TASK_NOT_RUNNING_OR_COMMITTED = -200473
    CAN_NOT_WRITE_WHEN_AUTO_START_FALSE_AND_TASK_NOT_RUNNING_OR_COMMITTED = -200472
    CAN_NOT_WRITE_NOT_STARTED_AUTO_START_FALSE_NOT_ON_DEMAND_BUF_SIZE_ZERO = -200802
    CAN_NOT_WRITE_TO_FINITE_CO_TASK = -201291
    SAMPLES_NOT_YET_AVALIABLE = -200284
    SAMPLES_NO_LONGER_AVAILABLE = -200279
    SAMPLES_WILL_NEVER_BE_AVAILABLE = -200278
    RUNTIME_ABORTED_ROUTING = -88709
    TIMEOUT = -26802
    MIN_NOT_LESS_THAN_MAX = -200082
    INVALID_NUMBER_SAMPLES_TO_READ = -200096
    INVAILD_NUM_SAMPS_TO_WRITE = -200622
    DEVICE_NAME_NOT_FOUND_ROUTING = -88717
    INVALID_ROUNTING_SOURCE_TERMINAL_NAME_ROUTING = -89120
    INVALID_TERM_ROUTING = -89129
    UNSUPPORTED_SIGNAL_TYPE_EXPORT_SIGNAL = -200375
    CHANNEL_SIZE_TOO_BIG_FOR_U16_PORT_WRITE = -200879
    CHANNEL_SIZE_TOO_BIG_FOR_U16_PORT_READ = -200878
    CHANNEL_SIZE_TOO_BIG_FOR_U32_PORT_WRITE = -200566
    CHANNEL_SIZE_TOO_BIG_FOR_U8_PORT_WRITE = -200565
    CHANNEL_SIZE_TOO_BIG_FOR_U32_PORT_READ = -200564
    CHANNEL_SIZE_TOO_BIG_FOR_U8_PORT_READ = -200563
    WAIT_UNTIL_DONE_DOES_NOT_INDICATE_DONE = -200560
    AUTO_START_WRITE_NOT_ALLOWED_EVENT_REGISTERED = -200985
    AUTO_START_READ_NOT_ALLOWED_EVENT_REGISTERED = -200984
    EVERY_N_SAMPLES_ACQ_INTO_BUFFER_EVENT_NOT_SUPPORTED_BY_DEVICE = -200981
    EVERY_N_SAMPLES_TRANSFERRED_FROM_BUFFER_EVENT_NOT_SUPPORTED_BY_DEVICE = -200980
    CAN_NOT_REGISTER_ART_DAQ_SOFTWARE_EVENT_WHILE_TASK_RUNNING = -200960
    EVERY_N_SAMPLES_EVENT_NOT_SUPPORTED_FOR_NON_BUFFERED_TASKS = -200848
    EVERY_N_SAMPLES_EVENT_NOT_SUPPORTED = 200489
    BUFFER_SIZE_NOT_MULTIPLE_OF_EVERY_N_SAMPS_EVENT_INTERVAL_WHEN_DMA = -200877
    EVERY_N_SAMPS_TRANSFERRED_FROM_BUFFER_NOT_FOR_INPUT = -200965
    EVERY_N_SAMPS_ACQ_INTO_BUFFER_NOT_FOR_OUTPUT = -200964
    READ_NO_INPUT_CHANS_IN_TASK = -200460
    WRITE_NO_OUTPUT_CHANS_IN_TASK = -200459
    INVALID_TIMEOUT_VAL = -200453
    ATTRIBUTE_NOT_SUPPORTED_IN_TASK_CONTEXT = -200452
    NO_MORE_SPACE = -200293
    SAMPLES_CAN_NOT_YET_BE_WRITTEN = -200292
    GEN_STOPPED_TO_PREVENT_REGEN_OF_OLD_SAMPLES = -200290
    SAMPLES_WILL_NEVER_BE_GENERATED = -200288
    CANNOT_READ_RELATIVE_TO_REF_TRIG_UNTIL_DONE = -200281
    EXT_SAMP_CLK_SRC_NOT_SPECIFIED = -200303
    CANNOT_UPDATE_PULSE_GEN_PROPERTY = -200301
    INVALID_TIMING_TYPE = -200300
    INVALID_ANALOG_TRIG_SRC = -200265
    TRIG_WHEN_ON_DEMAND_SAMP_TIMING = -200262
    REF_TRIG_WHEN_CONTINUOUS = -200358
    SPECIFIED_ATTR_NOT_VALID = -200233
    OUTPUT_BUFFER_EMPTY = -200462
    INVALID_OPTION_FOR_DIGITAL_PORT_CHANNEL = -200376
    CTR_MIN_MAX = -200527
    WRITE_CHAN_TYPE_MISMATCH = -200526
    READ_CHAN_TYPE_MISMATCH = -200525
    WRITE_NUM_CHANS_MISMATCH = -200524
    ONE_CHAN_READ_FOR_MULTI_CHAN_TASK = -200523
    MULTIPLE_COUNTER_INPUT_TASK = -200147
    COUNTER_START_PAUSE_TRIGGER_CONFLICT = -200146
    COUNTER_INPUT_PAUSE_TRIGGER_AND_SAMPLE_CLOCK_INVALID = -200145
    COUNTER_OUTPUT_PAUSE_TRIGGER_INVALID = -200144
    FILE_NOT_FOUND = -26103
    NONBUFFERED_OR_NO_CHANNELS = -201395
    BUFFERED_OPERATIONS_NOT_SUPPORTED_ON_SELECTED_LINES = -201062
    CALIBRATION_FAILED = -200157
    INVALID_FILL_MODE_PARAMETER = -300001
    PHYS_CHAN_OUTPUT_TYPE = -200432
    PHYS_CHAN_MEAS_TYPE = -200431
    INVALID_PHYS_CHAN_TYPE = -200430
    SUITABLE_TIMEBASE_NOT_FOUND_TIME_COMBO_2 = -200746
    SUITABLE_TIMEBASE_NOT_FOUND_FREQUENCY_COMBO_2 = -200745
    UNKNOWN = -1


class Warnings(Enum):
    UNKNOWN = -1
    Returned_DATA_IS_NOT_ENOUGH = 30014
    CAPI_STRING_TRUNCATED_TO_FIT_BUFFER = 200026
