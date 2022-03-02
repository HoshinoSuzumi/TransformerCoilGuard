import pprint

import matplotlib.pyplot as plt

import artdaq
from artdaq.constants import AcquisitionType

pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__':
    with artdaq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Misaka/ai0")
        task.ai_channels.add_ai_voltage_chan("Misaka/ai1")
        task.timing.cfg_samp_clk_timing(15000, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=1000)

        u = task.read(number_of_samples_per_channel=1000)[0]
        i = task.read(number_of_samples_per_channel=1000)[1]

        plt.plot(u)
        plt.plot(i)
        plt.show()
