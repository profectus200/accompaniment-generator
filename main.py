"""Runs the script and finds the most fitting accompaniment for the given song."""

import mido
from mido import MetaMessage

import globals
from algorithm import evolution
from iohandler import get_notes, write_output_chords, get_tempo, get_tonic, compute_consonant_chords

midi_file = mido.MidiFile(globals.INPUT_FILE_NAME, clip=True)
midi_file.type = 1
globals.DURATION = midi_file.ticks_per_beat * 2

scale = get_tonic()
compute_consonant_chords(scale)
tempo = get_tempo(midi_file)
tracks = [MetaMessage('set_tempo', tempo=tempo, time=0)]
song_notes = get_notes(midi_file.tracks[1])

output_chords = evolution(song_notes)

write_output_chords(midi_file, tracks, output_chords)
