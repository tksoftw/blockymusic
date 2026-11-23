class Song:
    bpm: int
    beats: int
    note_list: list

    def __init__(self, bpm, beats):
        self.bpm = bpm
        self.beats = beats
        self.note_list = [0]*beats
        

song = ["em7", "b7", "dm", "g7", "cmaj9", "b7", "em7", "bm7", "b7",
        "am7", "b7", "b7", "em9", "em7"]

note_timing = [6,2,4,4,5,3,3,5,8,4,4,13]
