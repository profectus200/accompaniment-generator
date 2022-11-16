"""Implements functions which are working with input/output."""

import music21
from mido import Message, MetaMessage

import globals
from chord import Chord


def identify_music_scale():
    """
    Identifies music scale of the song.

    :return: scale of the song
    """
    score = music21.converter.parse(globals.INPUT_FILE_NAME)
    key = score.analyze('key')

    if key.mode == "minor":
        scale = (key.tonic.midi + 3) % 12
    else:
        scale = key.tonic.midi % 12
    return scale


def get_tempo(midi_file):
    """
    Computes tempo for the given song.

    :param midi_file: song to compute tempo
    :return: tempo of the song
    """
    tempo = 0

    for track in midi_file.tracks:
        for message in track:
            if isinstance(message, MetaMessage) and message.type == "set_tempo":
                tempo = message.tempo
    return tempo


def get_notes_amount(track):
    """
    Computes number of notes in the given track.

    :param track: track to compute number of notes
    :return: number of notes in the track
    """
    beats = 0

    for message in track:
        if type(message) is Message:
            beats += message.time

    return (beats + globals.DURATION - 1) // globals.DURATION


def identify_notes(track):
    """
    Identifies notes in the given track.

    :param track: track to compute identify notes
    :return: list of the identified notes
    """
    notes_list = [None] * get_notes_amount(track)
    beats, last_note = 0, 0

    for message in track:
        if type(message) is Message:
            if message.type == "note_off":
                last_note = message.note

            if beats % globals.DURATION == 0 and message.type == "note_on":
                if notes_list[beats // globals.DURATION] is None:
                    notes_list[beats // globals.DURATION] = message.note

            beats += message.time
    if beats % globals.DURATION == 0:
        notes_list[-1] = last_note
    return notes_list


def compute_consonant_chords(scale):
    """
    Computes consonant chords for the given scale using the circle of fifth.

    :param scale: the given scale
    :return: None
    """
    globals.CONSONANT_CHORDS = [Chord(scale % 12, globals.MAJOR_TRIAD),
                                Chord((scale + 5) % 12, globals.MAJOR_TRIAD),
                                Chord((scale + 7) % 12, globals.MAJOR_TRIAD),
                                Chord((scale + 9) % 12, globals.MINOR_TRIAD),
                                Chord((scale + 2) % 12, globals.MINOR_TRIAD),
                                Chord((scale + 4) % 12, globals.MINOR_TRIAD),
                                Chord((scale + 11) % 12, globals.DIM_CHORD)]


def get_average_velocity(midi_file):
    """
    Computes the averages velocity for the given song.

    :param midi_file: the given song
    :return: average velocity of the given song
    """
    note_number, velocity = 0, 0

    for message in midi_file.tracks[1]:
        if isinstance(message, Message) and message.type == 'note_on':
            note_number += 1
            velocity += message.velocity
    return int(velocity / note_number * 0.9)


def get_average_displacement(midi_file):
    """
    Computes the averages velocity for the given song.

    :param midi_file: the given song
    :return: average displacement of the given song
    """
    note_number, octave = 0, 0

    for message in midi_file.tracks[1]:
        if isinstance(message, Message) and message.type == 'note_on':
            note_number += 1
            octave += int(message.note / 12)
    return 12 * (int(octave / note_number) - 1)


def write_output_chords(midi_file, tracks, output_chords):
    """
    Writes output chords to the given song.

    :param midi_file: the given song
    :param tracks: new tracks to add
    :param output_chords: computed chords to add
    :return: None
    """
    velocity = get_average_velocity(midi_file)
    displacement = get_average_displacement(midi_file)

    for chord in output_chords:
        for i in range(3):
            tracks.append(
                Message('note_on', channel=0, note=chord.note_list[i] + displacement, velocity=velocity, time=0))
        tracks.append(Message('note_off', channel=0, note=chord.note_list[0] + displacement, velocity=velocity,
                              time=globals.DURATION))
        for i in range(1, 3):
            tracks.append(
                Message('note_off', channel=0, note=chord.note_list[i] + displacement, velocity=velocity, time=0))

    midi_file.tracks.append(tracks)
    midi_file.save(globals.OUTPUT_FILE_NAME)
