import json
import logging
import pprint
import time
from time import sleep as delay

from azure.iot.device import IoTHubDeviceClient, Message

import artdaq

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(level=logging.ERROR)

azureClient = IoTHubDeviceClient.create_from_connection_string(
    'HostName=TransformerCoilGuard.azure-devices.net;DeviceId=TCG_Gateway;SharedAccessKey=rLG7ePO'
    '+BFC60BgpdxKkX1pH3KuD0o2CUQJSxNh9CF8=')
print('Connecting Azure IoT Center...')
azureClient.connect()
print('Connected to Azure IoT Center')


def fake_message_handler(rev_msg):
    print('Message received')
    for prop in vars(rev_msg).items():
        print(prop)


if __name__ == '__main__':
    enable_fetching = True
    voltage_data_buff = []
    current_data_buff = []
    t_delta_sequences = []

    try:
        azureClient.on_message_received = fake_message_handler

        with artdaq.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Misaka/ai0")
            task.ai_channels.add_ai_voltage_chan("Misaka/ai1")

            t_start = time.time()
            while True:
                while enable_fetching:
                    read_data = task.read()
                    data_U3 = read_data[0]
                    data_I1 = read_data[1]
                    voltage_data_buff.append(data_U3)
                    current_data_buff.append(data_I1)
                    t_delta_sequences.append(time.time() - t_start)
                    enable_fetching = len(voltage_data_buff) <= 600

                data_dict = {
                    'voltages': voltage_data_buff,
                    'currents': current_data_buff
                }
                data_payload = json.dumps(data_dict, default=lambda o: o.__dict__, sort_keys=True)
                msg = Message(data_payload)
                msg.content_type = 'application/json'
                msg.content_encoding = 'utf-8'
                azureClient.send_message(msg)
                print('sending', msg)
                voltage_data_buff.clear()
                current_data_buff.clear()
                t_delta_sequences.clear()
                delay(600)
                enable_fetching = True
                t_start = time.time()

    except KeyboardInterrupt:
        print('Stopped')
    finally:
        print('Shutting down')
        azureClient.shutdown()
