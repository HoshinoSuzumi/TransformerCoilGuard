import pprint

import artdaq

pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__':

    with artdaq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Misaka/ai0")
        task.ai_channels.add_ai_voltage_chan("Misaka/ai1")
        while True:
            print('Sending %s' % task.read()[0])
