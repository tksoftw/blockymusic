import pyaudio
from pyaudio import paFloat32, paContinue
from numpy import pi, sin, arange, float32, zeros

engine = pyaudio.PyAudio()

class PySine:
    rate = 44100
    offset = 0
    def __init__(self, frequencies):
        self.frequencies = frequencies
        # Setup stream
        def play(in_data, frames, time_info, status):
            out = zeros(frames,dtype=float32)
            for freq in self.frequencies:
                out += sin((arange(frames,dtype=float32)+self.offset)*2*pi*float(freq)/self.rate)
            out /= len(self.frequencies)
            self.offset += frames
            return (out, paContinue)

        self.stream = engine.open(format=paFloat32,
            channels=1,
            rate=self.rate,
            output=True,
            stream_callback=play)

    def change_frequencies(self, new_freqs):
        self.frequencies = new_freqs
    
    def add_frequencies(self, freqs_to_add):
        self.frequencies.extend(freqs_to_add)

    def remove_frequency(self, freq_to_remove):
        self.frequencies.remove(freq_to_remove)

    # Redundant    
    # def start(self):
    #     self.stream.start_stream()
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

def sines(freqs):
    return PySine(freqs)

def sine(freq):
    return sines([freq])

def terminate():
    engine.terminate()

if __name__ == "__main__":
    from time import sleep

    wv = sines([369.92, 440.0, 493.92, 587.2, 293.6])
    
    import pygame
    screen = pygame.display.set_mode([640,480])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                print("!")
                wv.change_frequencies([100, 200, 300, 400, 500])
        sleep(0.0001)
    