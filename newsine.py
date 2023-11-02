from pyaudio import PyAudio, paContinue, paComplete
import numpy as np

def get_data_general(freq):
    points = 44100+324-72
    times = np.linspace(0, 1, points, endpoint=False)
    data = np.array((np.sin(times*freq*2*np.pi) + 1.0)*127.5, dtype=np.int8).tobytes()
    return data

class PySine(object):
    BITRATE = 44100+324-72.
    #CHUNK_SIZE = 1024  # Number of audio frames per buffer

    def __init__(self, frequency, duration, leave_open=False, extend_audio=False):
        self.pyaudio = PyAudio()
        self.duration = duration
        self.data = None
        self.data_index = 0  # Keep track of how much data we've played
        self.leave_open = leave_open
        self.extend_audio = extend_audio

        # Define callback function
        def callback(in_data, frame_count, time_info, status):
            end_index = self.data_index + frame_count
            chunk = self.data[self.data_index:end_index]
            self.data_index += len(chunk)
            
            # if len(chunk) < frame_count:  # If chunk is smaller than requested, pad with zeros
            #     chunk += b'\x00' * (frame_count - len(chunk))
            
            if self.data_index >= len(self.data) and self.extend_audio:
                self.data_index = 0
                return (chunk, paContinue)
            elif self.data_index >= len(self.data) and not self.leave_open:
                return (chunk, paComplete)
            else:
                return (chunk, paContinue)
        
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(1),
            channels=1,
            rate=int(self.BITRATE),
            output=True,
            stream_callback=callback)

    def change_dur(self, new_dur):
        self.duration = new_dur

    def change_freq(self, new_freq):
        self.data_index = 0
        self.data = self.get_data(new_freq)

    def get_data(self, frequency):
        points = int(self.BITRATE * self.duration)
        times = np.linspace(0, self.duration, points, endpoint=False)
        data = np.array((np.sin(times*frequency*2*np.pi) + 1.0)*127.5, dtype=np.int8).tobytes()
        return data

    def play(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

data_store = {}
channels = {}
def start_sine(freq=400):
    if freq in channels:
        channels[freq].play()
    else:
        wave = PySine(freq, 1, leave_open=True, extend_audio=True)
        wave.data = data_store[freq] if freq in data_store else wave.get_data(freq)
        wave.play()
        channels[freq] = wave

def prepare_sine(freq):
    data_store[freq] = get_data_general(freq)

def end_sine(ch_id):
    if ch_id in channels:
        channels[ch_id].stop()

def sin(freq, dur=0.1, extend=False):
    if len(channels) == 0:
        wave = PySine(freq, dur, leave_open=True, extend_audio=extend)
        channels.append(wave)
        channels[0].play()
    else:
        channels[0].change_freq(freq)

def sine(freq, dur=1):
    channel = PySine(freq, dur)
    channel.play()

if __name__ == '__main__':
    # C major chord
    # sine(261.6256, 1)
    # sine(329.6276, 1)
    # sine(391.9954, 1)
    
    # # Bullseye
    # sine(36.70810) # D1
    # sine(73.41619) # D2
    # sine(329.6276) # D4
    # sine(369.9944) # F#4
    # sine(440) # A4
    # sine(493.8833) # B4
    # sine(587.3295) # D5
    pass