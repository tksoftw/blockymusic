import newsine as nw
import time

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

def play_note(note, dur=0.25):
    freq = get_note_freq(note)
    nw.sine(freq, duration=dur)

def play_notes_old(notesAndOcts, dur=0.25):
    #dur *= 3
    for note, octave in notesAndOcts:
        play_note(note + str(octave), dur)
    time.sleep(dur)

def play_notes(notes, dur=0, sleep=True):
    for note in notes:
        play_note(note, dur)

def play_song(rHand, lHand, noteNps):
    for noteR, noteL, nps in zip(rHand, lHand, noteNps):
        for i, note in enumerate([noteR, noteL]):
            # if note[:-1] == 'C':
            #     play_chord(note, dur=nps)
            if note != '-':
                play_note(note, dur=nps)
        time.sleep(nps)

def play_chord(chord, dur=1):
    note, octave = chord[:-1], chord[-1]
    chords = {
        'C': ('C', 'E', 'G'),
    }
    # Add octave
    notes = []
    for note in chords[note]:
        notes.append(note + octave)
    play_notes(notes, dur)

def play_note_on_key(note, key):
    pass


if __name__ == '__main__':
    # C major3
    chord = ['C3','E3','G3']

    # Jingle Bell Rock
    rHand = ['C5','-','C5','C5','-','-','B4','-','B4','B4','-','-','A4','-','B4','A4','-','-','-','E4']
    lHand = ['C4','-','C4','C4','-','-','B3','-','B3','B3','-','-','A3','-','B3','A3','-','-','-','E3']
    nps = 1/6
    noteScalars = [nps]*(len(lHand)-1) + [nps*4]
    print(noteScalars)
    play_song(rHand, lHand, noteScalars)

    # Megalovania
    # play_notes_old([("D", 3), ("D", 2)], .12)
    # play_notes_old([("D", 3), ("D", 2)], .12)
    # play_notes_old([("D", 4), ("D", 2)], .2)
    # play_notes_old([("A", 3), ("D", 2)], .3)
    # play_notes_old([("Ab", 3), ("D", 2)], .2)
    # play_notes_old([("G", 3), ("D", 2)], .2)
    # play_notes_old([("F", 3), ("D", 2)], .2)
    # play_notes_old([("D", 3), ("D", 2)], .12)
    # play_notes_old([("F", 3), ("D", 2)], .1)
    # play_notes_old([("G", 3), ("D", 2)], .1)

    # time.sleep(0.1)

    # play_notes_old([("C", 3), ("C", 2)], .12)
    # play_notes_old([("C", 3), ("C", 2)], .12)
    # play_notes_old([("D", 4), ("C", 2)], .2)
    # play_notes_old([("A", 3), ("C", 2)], .3)
    # play_notes_old([("Ab", 3), ("C", 2)], .2)
    # play_notes_old([("G", 3), ("C", 2)], .2)
    # play_notes_old([("F", 3), ("C", 2)], .2)
    # play_notes_old([("D", 3), ("C", 2)], .12)
    # play_notes_old([("F", 3), ("C", 2)], .1)
    # play_notes_old([("G", 3), ("C", 2)], .1)

    # time.sleep(0.1)

    # play_notes_old([("B", 2), ("B", 1)], .12)
    # play_notes_old([("B", 2), ("B", 1)], .12)
    # play_notes_old([("D", 4), ("B", 1)], .2)
    # play_notes_old([("A", 3), ("B", 1)], .3)
    # play_notes_old([("Ab", 3), ("B", 1)], .2)
    # play_notes_old([("G", 3), ("B", 1)], .2)
    # play_notes_old([("F", 3), ("B", 1)], .2)
    # play_notes_old([("D", 3), ("B", 1)], .12)
    # play_notes_old([("F", 3), ("B", 1)], .1)
    # play_notes_old([("G", 3), ("B", 1)], .1)

    # time.sleep(0.1)

    # play_notes_old([("Bb", 2), ("Bb", 1)], .12)
    # play_notes_old([("Bb", 2), ("Bb", 1)], .12)
    # play_notes_old([("D", 4), ("Bb", 1)], .2)
    # play_notes_old([("A", 3), ("Bb", 1)], .3)
    # play_notes_old([("Ab", 3), ("Bb", 1)], .2)
    # play_notes_old([("G", 3), ("Bb", 1)], .2)
    # play_notes_old([("F", 3), ("Bb", 1)], .2)
    # play_notes_old([("D", 3), ("Bb", 1)], .12)
    # play_notes_old([("F", 3), ("Bb", 1)], .1)
    # play_notes_old([("G", 3), ("Bb", 1)], .1)