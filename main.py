import pprint

import artdaq
from artdaq.constants import AcquisitionType

pp = pprint.PrettyPrinter(indent=4)

with artdaq.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Misaka/ai0")
    task.timing.cfg_samp_clk_timing(500, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=50)
    for _ in range(1):
        data = task.read(number_of_samples_per_channel=10)
        print("Data:")
        pp.pprint(data)
