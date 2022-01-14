import json
import time

import matplotlib.pyplot as plt
from azure.iot.device import IoTHubDeviceClient, Message
from numpy import *
from numpy.fft import *

import artdaq
from artdaq.constants import AcquisitionType


def acquire_ui(samples, rate=15000):
    with artdaq.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Misaka/ai0')
        task.ai_channels.add_ai_voltage_chan('Misaka/ai1')
        task.timing.cfg_samp_clk_timing(rate, sample_mode=AcquisitionType.FINITE, samps_per_chan=1000)

        acquired_data = task.read(number_of_samples_per_channel=samples)
        u_sequence = acquired_data[0]
        i_sequence = acquired_data[1]
        return u_sequence, i_sequence


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
    # x = linspace(0, 1, 15000)
    # signal_u = 4 * sin(2 * pi * 50 * x)
    # signal_i = 0.005 * sin(2 * pi * 50 * (x + random.normal(0, 0.5, 15000)))

    time_increment = 0

    azureClient = IoTHubDeviceClient.create_from_connection_string(
        'HostName=TransformerCoilGuard.azure-devices.net;DeviceId=TCG_Gateway;SharedAccessKey=rLG7ePO'
        '+BFC60BgpdxKkX1pH3KuD0o2CUQJSxNh9CF8=')
    print('Connecting Azure IoT Center...')
    azureClient.connect()
    print('Connected to Azure IoT Center')

    while True:
        # 15000 data/s
        U, I = acquire_ui(1000, rate=15000)
        X, Y = lissajous_figure_calc(U, I, 15000, 50, 1000)

        data_dict = {
            'lissajous': {
                'X': X.tolist(),
                'Y': Y.tolist()
            },
            'voltages': U,
            'currents': I
        }
        data_payload = json.dumps(data_dict)
        msg = Message(data_payload)
        msg.content_type = 'application/json'
        msg.content_encoding = 'utf-8'
        azureClient.send_message(msg)
        print('Sent', msg)

        plt.subplot(221)
        plt.title('Sampling U & I')
        plt.plot(U)
        plt.plot(I)

        plt.subplot(222)
        plt.title('Lissajous figure')
        plt.plot(X, Y)

        plt.subplot(223)
        plt.title('Acquired data U')
        plt.plot(U)

        plt.subplot(224)
        plt.title('Acquired data I')
        plt.plot(I)

        plt.show()

        time.sleep(600)
