"""Runs the script and finds the most fitting accompaniment for the given song."""

import mido
from mido import MetaMessage

import globals
from algorithm import evolution
from iohandler import get_notes, write_output_chords, get_tempo, get_tonic, compute_consonant_chords, get_input_files


def compute_accompaniment():
    """
    Identifies and adds accompaniment to the given song.

    :return: None
    """
    input_files = get_input_files()
    for i in range(len(input_files)):
        input_file = input_files[i]
        midi_file = mido.MidiFile(input_file, clip=True)
        midi_file.type = 1
        globals.DURATION = midi_file.ticks_per_beat * 2

        tonic = get_tonic(input_file)
        compute_consonant_chords(tonic)
        tempo = get_tempo(midi_file)
        tracks = [MetaMessage('set_tempo', tempo=tempo, time=0)]
        song_notes = get_notes(midi_file.tracks[1])

        output_chords = evolution(song_notes)

        write_output_chords(midi_file, tracks, output_chords, input_file, i)


compute_accompaniment()
