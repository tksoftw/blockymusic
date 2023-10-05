from pyaudio import PyAudio, paContinue, paComplete
import numpy as np
import time

class PySine(object):
    BITRATE = 96000.
    CHUNK_SIZE = 1024  # Number of audio frames per buffer

    def __init__(self, frequency, duration):
        self.pyaudio = PyAudio()
        self.frequency = frequency
        self.duration = duration
        self.data = self.get_data()
        self.data_index = 0  # Keep track of how much data we've played

        # Define callback function
        def callback(in_data, frame_count, time_info, status):
            end_index = self.data_index + frame_count
            chunk = self.data[self.data_index:end_index]
            self.data_index += len(chunk)
            
            if len(chunk) < frame_count:  # If chunk is smaller than requested, pad with zeros
                chunk += b'\x00' * (frame_count - len(chunk))
            
            if self.data_index >= len(self.data):
                return (chunk, paComplete)
            else:
                return (chunk, paContinue)
        
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(1),
            channels=1,
            rate=int(self.BITRATE),
            output=True,
            stream_callback=callback)

    def get_data(self):
        points = int(self.BITRATE * self.duration)
        times = np.linspace(0, self.duration, points, endpoint=False)
        data = np.array((np.sin(times*self.frequency*2*np.pi) + 1.0)*127.5, dtype=np.int8).tobytes()
        return data

    def play(self):
        self.stream.start_stream()

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

def sine(frequency=440.0, duration=1.0):
    wave = PySine(frequency, duration)
    wave.play()


if __name__ == '__main__':
    # C major chord
    # sine(261.6256, 1)
    # sine(329.6276, 1)
    # sine(391.9954, 1)
    
    # Bullseye
    sine(36.70810) # D1
    sine(73.41619) # D2
    sine(329.6276) # D4
    sine(369.9944) # F#4
    sine(440) # A4
    sine(493.8833) # B4
    sine(587.3295) # D5
    


    time.sleep(1)  # Extend sleep slightly to ensure playback completes
