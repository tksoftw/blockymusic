import pysinenew
import time
import pygame
pygame.init()

def get_note_freq(note):
    octave = int(note[-1])
    note = note[:-1]

    notes = {
        "C": 16.35,
        "C#": 17.32,
        "Db": 17.32,
        "D": 18.35,
        "D#": 19.45,
        "Eb": 19.45,
        "Eb": 19.45,
        "E": 20.60,
        "F": 21.83,
        "F#": 23.12,
        "Gb": 23.12,
        "G": 24.50,
        "G#": 25.96,
        "G#": 25.96,
        "Ab": 25.96,
        "A": 27.50,
        "A#": 29.14,
        "Bb": 29.14,
        "B": 30.87,
    }

    # Adjust for octaves
    oct_adjusted_freq = notes[note] * (2 ** octave)
    return oct_adjusted_freq

def play_note(note, duration=1):
    note_freq = get_note_freq(note)
    wave = pysinenew.sine(note_freq)
    time.sleep(duration)
    wave.stop()

def play_chord(chord, duration=1, custom_player=None, custom_stopper=None):
    if custom_player and custom_stopper:
        custom_player(chord)
        time.sleep(duration)
        custom_stopper(chord)
    else:
        note_freqs = [get_note_freq(note) for note in chord]
        wave = pysinenew.sines(note_freqs)
        time.sleep(duration)
        wave.stop()

def increase_note_octave(note):
    return note[:-1] + str(int(note[-1])+1)

def increase_chord_octave(chord):
    new_chord = []
    for note in chord:
        new_chord.append(increase_note_octave(note))
    return tuple(new_chord)

def songify(note_and_chord_list, bpm):
    nps = (bpm*2)/60
    spn = 1/nps

    new_list = []
    for item in note_and_chord_list:
        to_add = item if type(item) != str else (item,)
        new_list.append(to_add)
    new_list.append(spn)
    return new_list

def increase_song_octave(song):
    for i, chord in enumerate(song[:-1]):
        if chord[0] != '_':
            song[i] = increase_chord_octave(chord)


def play_song(custom_player=None, custom_stopper=None):
    cMaj4 = ("C4", "E4", "G4")
    aMaj3 = ("A3", "C4", "E4")
    fMaj3 = ("F3", "A3", "C4")
    gMaj3 = ("G3", "B3", "D4")

    bpm = 108
    heart_and_soul = ['C3', '_', 'C3', cMaj4, '_', cMaj4,
                       'A2', '_', 'A2', aMaj3, '_', aMaj3,
                         'F2', '_', 'F2', fMaj3, '_', fMaj3,
                           'G2', '_', 'G2', gMaj3, '_', gMaj3]

    bpm *= 2
    sg = songify(heart_and_soul, bpm)
    increase_song_octave(sg)
    spn = sg.pop()
    for item in sg:
        if item[0] == '_':
            time.sleep(spn)
            continue
        play_chord(item, spn, custom_player, custom_stopper)
    time.sleep(1)

class piano:
    def __init__(self):
        self.screen =  pygame.display.set_mode((640,480))

        self.key_map = {
            pygame.K_a: "C4",
            pygame.K_s: "D4",
            pygame.K_d: "E4",
            pygame.K_f: "F4",
            pygame.K_g: "G4",
            pygame.K_h: "A4",
            pygame.K_j: "B4",
            pygame.K_k: "C5",
            pygame.K_l: "D5",
            pygame.K_SEMICOLON: "E5",
            pygame.K_QUOTE: "F5",

            pygame.K_w: "C#4",
            pygame.K_e: "D#4",
            pygame.K_t: "F#4",
            pygame.K_y: "G#4",
            pygame.K_u: "A#4",
            pygame.K_o: "C#5",
            pygame.K_p: "D#5",
            pygame.K_RIGHTBRACKET: "F#5"
        }

        self.picture = pygame.image.load('piano.jpg')
        self.picture = pygame.transform.scale(self.picture, pygame.display.get_surface().get_size())
        self.screen.blit(self.picture, self.picture.get_rect())
        pygame.display.update()

        self.cur_displayed_notes = set()
        self.cur_wave = pysinenew.sine(0)
        self.cur_octave = 4
    
    def run(self):
        played = False
        while True:
            time.sleep(0.0001)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    played = False
                    self.shift_octave(1)
                    self.cur_octave += 1
                    print("current octave:", self.key_map[pygame.K_a][-1])
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.shift_octave(-1)
                    self.cur_octave -= 1
                    print("current octave:", self.key_map[pygame.K_a][-1])
                if event.type == pygame.KEYDOWN and event.key in self.key_map:
                    self.press_note(self.key_map[event.key])
                if event.type == pygame.KEYUP and event.key in self.key_map and self.cur_wave is not None and get_note_freq(self.key_map[event.key]) in self.cur_wave.frequencies:
                    self.release_note(self.key_map[event.key])
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z and not played:
                    played = True
                    self.custom_event()


    def set_custom(self, func, *args):
        self.custom_event = lambda : func(*args)

    def press_notes(self, notes):
        new_freqs = [get_note_freq(note) for note in notes]
        self.cur_wave.add_frequencies(new_freqs)
        self.draw_notes(notes)
        self.cur_displayed_notes.update(notes)

    def press_note(self, note):
        new_freqs = [*self.cur_wave.frequencies, get_note_freq(note)]
        self.cur_wave.change_frequencies(new_freqs)
        self.draw_note(note)
        self.cur_displayed_notes.add(note)

    def release_note(self, note):
        self.release_notes([note])

    def release_notes(self, notes):
        for note in notes:
            self.cur_wave.remove_frequency(get_note_freq(note))
            self.cur_displayed_notes.remove(note)
        self.redraw()

    def shift_octave(self, offset):
        for k, v in self.key_map.copy().items():
            self.key_map[k] = v[:-1] + str((int(v[-1])+offset)%10)

    def draw_note(self, note):
        self.draw_notes([note])
    
    def draw_notes(self, notes):
        for note in notes:
            note, octave = note[:-1], int(note[-1])
            key_positions = {
                "C": (50, 400),
                "D": (100, 400),
                "E": (150, 400), 
                "F": (200, 400), 
                "G": (250, 400), 
                "A": (300, 400), 
                "B": (350, 400), 
                #"C": (400, 400), 

                "C#": (55, 300),
                "D#": (125, 300),
                "F#": (215, 300),
                "G#": (275, 300),
                "A#": (335, 300)
            }
            x_increase = (octave-self.cur_octave)*360
            light_coords = [key_positions[note][0]+x_increase, key_positions[note][1]]

            shift_direction = 1 if light_coords[0] < 0 else -1
            while light_coords[0] < 0 or light_coords[0] > self.screen.get_rect().right:
                light_coords[0] += shift_direction*360

            light = pygame.Rect(light_coords, (10,10))
            pygame.draw.rect(self.screen, 'red', light)
        pygame.display.update()

    def redraw(self):
        self.screen.blit(self.picture, self.picture.get_rect())
        if self.cur_displayed_notes is not None:
            for note in self.cur_displayed_notes:
                self.draw_note(note)
        pygame.display.update()

# def pian2o():
#     screen =  pygame.display.set_mode((640,480))

#     key_map = {
#         pygame.K_a: "C4",
#         pygame.K_s: "D4",
#         pygame.K_d: "E4",
#         pygame.K_f: "F4",
#         pygame.K_g: "G4",
#         pygame.K_h: "A4",
#         pygame.K_j: "B4",
#         pygame.K_k: "C5",
#         pygame.K_l: "D5",
#         pygame.K_SEMICOLON: "E5",
#         pygame.K_QUOTE: "F5",

#         pygame.K_w: "C#4",
#         pygame.K_e: "D#4",
#         pygame.K_t: "F#4",
#         pygame.K_y: "G#4",
#         pygame.K_u: "A#4",
#         pygame.K_o: "C#5",
#         pygame.K_p: "D#5",
#         pygame.K_RIGHTBRACKET: "F#5"
#     }

#     picture = pygame.image.load('piano.jpg')
#     picture = pygame.transform.scale(picture, pygame.display.get_surface().get_size())
#     screen.blit(picture, picture.get_rect())
#     pygame.display.update()

#     cur_displayed_notes = {}
#     cur_wave = pysinenew.sine(0)
#     cur_octave = 4
#     while True:
#         time.sleep(0.0001)
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
#                 change_octave(key_map, 1)
#                 cur_octave += 1
#                 print("current octave:", key_map[pygame.K_a][-1])
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
#                 change_octave(key_map, -1)
#                 cur_octave -= 1
#                 print("current octave:", key_map[pygame.K_a][-1])
#             if event.type == pygame.KEYDOWN and event.key in key_map:
#                 new_freqs = [*cur_wave.frequencies, get_note_freq(key_map[event.key])]
#                 cur_wave.change_frequencies(new_freqs)
#                 draw_note_indicator(screen, key_map[event.key], base_octave=cur_octave)
#                 cur_displayed_notes[key_map[event.key]] = cur_octave
#             if event.type == pygame.KEYUP and event.key in key_map and cur_wave is not None and get_note_freq(key_map[event.key]) in cur_wave.frequencies:
#                 cur_wave.remove_frequency(get_note_freq(key_map[event.key]))
#                 del cur_displayed_notes[key_map[event.key]]
#                 reset_screen(screen, picture, notes_displayed=cur_displayed_notes)

if __name__ == "__main__":
    #play_song()
    p = piano()
    p.set_custom(play_song, p.press_notes, p.release_notes)
    p.run()
    # note = 'C4'
    # chord = ['C4', 'E4', 'G4']
    # play_note(note, 0.25)
    # play_note(note, 0.25)
    # play_note(note, 0.25)
    # play_note(note, 0.25)
    # play_note(note, 0.25)
    # play_chord(chord, 0.25)
    # play_chord(chord, 0.25)
    # play_chord(chord, 0.25)
    # play_chord(chord, 0.25)
    # play_chord(chord, 0.25)