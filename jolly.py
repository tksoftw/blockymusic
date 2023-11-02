import time
import pygame
from fun import get_note_freq
from newsine import start_sine, end_sine, prepare_sine, data_store

def change_octave(key_map, offset):
    for k, v in key_map.copy().items():
        key_map[k] = v[:-1] + str((int(v[-1])+offset)%10)

def draw_note_indicator(screen, note, base_octave=4):
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
    x_increase = (octave-base_octave)*360
    light_coords = key_positions[note][0]+x_increase, key_positions[note][1]

    light = pygame.Rect(light_coords, (10,10))
    pygame.draw.rect(screen, 'red', light)
    pygame.display.update()

def reset_screen(screen, image):
    screen.blit(image, image.get_rect())
    pygame.display.update()

def play_note(note, duration=1):
    note_freq = get_note_freq(note)
    start_sine(note_freq)
    time.sleep(duration)
    end_sine(note_freq)

def play_chord(chord, duration=1):
    note_freqs = [get_note_freq(note) for note in chord[:-1]]
    for freq in note_freqs:
        start_sine(freq)
    time.sleep(duration)
    for freq in note_freqs:
        end_sine(freq)

def prepare_song(song):
    for item in song:
        if type(item) == str and item != '_':
            prepare_sine(get_note_freq(item))
        else:
            for note in item:
                if note != '_':
                    prepare_sine(get_note_freq(note))

def play_song():
    cMaj4 = ("C4", "E4", "G4")
    aMaj3 = ("A3", "C4", "E4")
    fMaj3 = ("F3", "A3", "C4")
    gMaj3 = ("G3", "B3", "D4")

    bpm = 108
    nps = (bpm*2)/60

    nps *= 2

    time_between_notes = 1/nps
    print(time_between_notes)
    heart_and_soul = ['C3', '_', 'C3', cMaj4, '_', cMaj4,
                       'A2', '_', 'A2', aMaj3, '_', aMaj3,
                         'F2', '_', 'F2', fMaj3, '_', fMaj3,
                           'G2', '_', 'G2', gMaj3, '_', gMaj3]
    
    print(len(data_store))
    prepare_song(heart_and_soul)
    print(len(data_store))
    for item in heart_and_soul:
        if type(item) == str:
            if item != '_':
                play_note(item, time_between_notes)
            else:
                time.sleep(time_between_notes)
        else:
            play_chord(item, time_between_notes)

if __name__ == "__main__":
    pygame.init()
    screen =  pygame.display.set_mode((640,480))

    key_map = {
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

    picture = pygame.image.load('piano.jpg')
    picture = pygame.transform.scale(picture, pygame.display.get_surface().get_size())
    screen.blit(picture, picture.get_rect())
    pygame.display.update()


    note = 'C4'
    chord = ['C4', 'E4', 'G4']
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

    cur_octave = 4
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                change_octave(key_map, 1)
                cur_octave += 1
                print("current octave:", key_map[pygame.K_a][-1])
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                change_octave(key_map, -1)
                cur_octave -= 1
                print("current octave:", key_map[pygame.K_a][-1])
            if event.type == pygame.KEYDOWN and event.key in key_map:
                start_sine(get_note_freq(key_map[event.key]))
                draw_note_indicator(screen, key_map[event.key], base_octave=cur_octave)
            elif event.type == pygame.KEYUP and event.key in key_map:
                end_sine(get_note_freq(key_map[event.key]))
                reset_screen(screen, picture)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                play_song()
                





    #time.sleep(1)  # Extend sleep slightly to ensure playback completes
