import json
import time

import matplotlib.pyplot as plt
from azure.iot.device import IoTHubDeviceClient, Message
from numpy import *
from numpy.fft import *

import artdaq
from artdaq.constants import AcquisitionType


def acquire_ui(samples, rate=15000, fake_data=False):
    if fake_data:
        x = linspace(0, 1, rate)
        a_u_sequence = 4 * sin(2 * pi * 50 * x)
        a_i_sequence = 0.005 * sin(2 * pi * 50 * (x + random.normal(0, 0.5, rate)))
        b_u_sequence = 4 * sin(2 * pi * 50 * x)
        b_i_sequence = 0.005 * sin(2 * pi * 50 * (x + random.normal(0, 0.4, rate)))
        c_u_sequence = 4 * sin(2 * pi * 50 * x)
        c_i_sequence = 0.005 * sin(2 * pi * 50 * (x + random.normal(0, 0.6, rate)))
        return {
            'A': [a_u_sequence, a_i_sequence],
            'B': [b_u_sequence, b_i_sequence],
            'C': [c_u_sequence, c_i_sequence],
        }

    with artdaq.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Misaka/ai0')
        task.ai_channels.add_ai_voltage_chan('Misaka/ai1')
        task.timing.cfg_samp_clk_timing(rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=1000)

        acquired_data = task.read(number_of_samples_per_channel=samples)
        a_u_sequence = acquired_data[0]
        a_i_sequence = acquired_data[1]
        return a_u_sequence, a_i_sequence


def fft_ma_calculate(s, fs, n1, f1):
    S1 = fft(s, n1)
    A = angle(S1[int(f1 * n1 / fs + 1)])
    M = abs(S1[int(f1 * n1 / fs + 1)]) * 2 / n1
    return M, A


def lissajous_figure_calc(signal_u, signal_i, fs=1200, f1=50, n1=600):
    t = (zeros(n1) + range(n1)) / fs

    m_u, a_u = fft_ma_calculate(signal_u, fs, n1, f1)
    m_i, a_i = fft_ma_calculate(signal_i, fs, n1, f1)

    X = m_u * cos(2 * pi * f1 * t + a_u)
    Y = m_i * cos(2 * pi * f1 * t + a_i)
    return X, Y


if __name__ == '__main__':
    time_increment = 0

    azureClient = IoTHubDeviceClient.create_from_connection_string(
        'HostName=TransformerCoilGuard.azure-devices.net;DeviceId=TCG_Gateway;SharedAccessKey=rLG7ePO'
        '+BFC60BgpdxKkX1pH3KuD0o2CUQJSxNh9CF8=')
    print('Connecting Azure IoT Center...')
    azureClient.connect()
    print('Connected to Azure IoT Center')

    while True:
        # 15000 data/s
        UA, IA = acquire_ui(1000, rate=15000, fake_data=False)['A']
        UB, IB = acquire_ui(1000, rate=15000, fake_data=False)['B']
        UC, IC = acquire_ui(1000, rate=15000, fake_data=False)['C']
        XA, YA = lissajous_figure_calc(UA, IA, 15000, 50, 1000)
        XB, YB = lissajous_figure_calc(UB, IB, 15000, 50, 1000)
        XC, YC = lissajous_figure_calc(UC, IC, 15000, 50, 1000)

        data_dict = {
            'lissajous': {
                "A": {
                    "X": XA.tolist(),
                    "Y": YA.tolist()
                },
                "B": {
                    "X": XB.tolist(),
                    "Y": YB.tolist()
                },
                "C": {
                    "X": XC.tolist(),
                    "Y": YC.tolist()
                }
            }
        }
        data_payload = json.dumps(data_dict)
        msg = Message(data_payload)
        msg.content_type = 'application/json'
        msg.content_encoding = 'utf-8'
        azureClient.send_message(msg)
        print('Sent', msg)

        plt.subplot(221)
        plt.title('Sampling U & I')
        plt.plot(UA)
        plt.plot(IA)

        plt.subplot(222)
        plt.title('Lissajous figure')
        plt.plot(XA, YA)

        plt.subplot(223)
        plt.title('Acquired data U')
        plt.plot(UA)

        plt.subplot(224)
        plt.title('Acquired data I')
        plt.plot(IA)

        plt.show()

        time.sleep(600)
