import os
from pyaudio import PyAudio
try:
    import numpy as np
except:
    from math import sin, pi
import time

class PySine(object):
    BITRATE = 96000.

    def __init__(self):
        self.pyaudio = PyAudio()
        try:
            self.stream = self.pyaudio.open(
                format=self.pyaudio.get_format_from_width(1),
                channels=1,
                rate=int(self.BITRATE),
                output=True)
        except:
            # output stream simulation with magicmock
            try:
                from mock import MagicMock
            except:  # python > 3.3
                from unittest.mock import MagicMock
            from time import sleep
            self.stream = MagicMock()
            def write(array):
                duration = len(array)/float(self.BITRATE)
                sleep(duration)
                print('\nHELLO\n')
                print(array)
                os.system('pause')
            self.stream.write = write

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

    def sine(self, frequency=440.0, duration=1.0):
        points = int(self.BITRATE * duration)
        try:
            times = np.linspace(0, duration, points, endpoint=False)
            data = np.array((np.sin(times*frequency*2*np.pi) + 1.0)*127.5, dtype=np.int8).tostring()
        except:  # do it without numpy
            data = ''
            omega = 2.0*pi*frequency/self.BITRATE
            for i in range(points):
                data += chr(int(127.5*(1.0+sin(float(i)*omega))))
        self.stream.write(data)

PYSINE = PySine()


def sine(frequency=440.0, duration=1.0):
    return PYSINE.sine(frequency=frequency, duration=duration)

if __name__ == '__main__':
    sine(400, 1)
    #time.sleep(1.5)  # Extend sleep slightly to ensure playback completes