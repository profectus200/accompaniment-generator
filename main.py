import mido
from mido import MetaMessage

import globals
from algorithm import evolution
from iohandler import determine_notes, write_output_chords, get_tempo, identify_music_scale, compute_consonant_chords

mid = mido.MidiFile(globals.INPUT_FILE_NAME, clip=True)
mid.type = 1
globals.DURATION = mid.ticks_per_beat * 2

identify_music_scale()
tempo = get_tempo(mid)
tracks = [MetaMessage('set_tempo', tempo=tempo, time=0)]
song_notes = determine_notes(mid.tracks[1])
compute_consonant_chords()

output_chords = evolution(globals.POPULATION_SIZE, song_notes)

write_output_chords(mid, tracks, output_chords)
