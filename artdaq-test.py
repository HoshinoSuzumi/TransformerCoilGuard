import pprint
import time

import artdaq

pp = pprint.PrettyPrinter(indent=4)

if __name__ == '__main__':

    with artdaq.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Misaka/ai0")
        task.ai_channels.add_ai_voltage_chan("Misaka/ai1")

        buffer = []

        st = time.time()
        ed = 0

        run = True

        while run:
            ed = time.time()
            if ed - st >= 0.207:
                run = False
            buffer.append(task.read()[0])
            # print('Sending %s' % task.read()[0])

        print("Time: %s\nData Points: %s", (ed - st, len(buffer)))
