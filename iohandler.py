"""Implements functions which are working with input/output."""

import music21
from mido import Message, MetaMessage

import globals
from chord import Chord


def get_input_files():
    """
    Gets input files names from the input.

    :return: input files names
    """
    mode = 2
    while True:
        try:
            mode = int(input("\nIf you want to enter specific file names enter '1'\n"
                             "If you want to use default file names enter '2'\nMode: "))
            if mode != 1 and mode != 2:
                raise ValueError
        except ValueError:
            print("Wrong mode format. Try again")
            continue
        break

    input_files = ['input/input1.mid', 'input/input2.mid', 'input/input3.mid']
    if mode == 1:
        input_files, n = [], 0
        while True:
            try:
                n = int(input("\nEnter the positive number of files for the accompaniment selection: "))
                if n < 0:
                    raise ValueError
            except ValueError:
                print("Wrong number of files format. Try again")
                continue
            break

        for i in range(n):
            input_files.append(input(f"Enter file name of the file №{i + 1}: "))
    return input_files


def get_tonic(input_file):
    """
    Identifies tonic of the song.

    :param input_file: input file name
    :return: tonic of the song
    """
    key = music21.converter.parse(input_file).analyze('key')
    if key.mode == "major":
        tonic = key.tonic.midi % 12
    else:
        tonic = (key.tonic.midi + 3) % 12
    return tonic


def get_key(input_file):
    """
    Identifies key of the song.

    :param input_file: input file name
    :return: key of the song
    """
    key = music21.converter.parse(input_file).analyze('key')
    if key.mode == "major":
        return key.tonic.name
    else:
        return key.tonic.name + "m"


def get_tempo(midi_file):
    """
    Identifies tempo for the given song.

    :param midi_file: song to compute tempo
    :return: tempo of the song
    """
    song_tempo = 0

    for track in midi_file.tracks:
        for message in filter(lambda x: type(x) is MetaMessage, track):
            if message.type == "set_tempo":
                song_tempo = message.tempo
    return song_tempo


def get_notes_amount(track):
    """
    Computes number of notes in the given track.

    :param track: track to compute number of notes
    :return: number of notes in the track
    """
    total_time = 0

    for message in filter(lambda x: type(x) is Message, track):
        total_time += message.time

    return (total_time + globals.DURATION - 1) // globals.DURATION


def get_notes(track):
    """
    Identifies notes in the given track.

    :param track: track to compute identify notes
    :return: list of the identified notes
    """
    notes_list = [None for _ in range(get_notes_amount(track))]
    total_time, final_note = 0, 0

    for message in filter(lambda x: type(x) is Message, track):
        if message.type == "note_off":
            final_note = message.note

        if total_time % globals.DURATION == 0 and message.type == "note_on":
            if notes_list[total_time // globals.DURATION] is None:
                notes_list[total_time // globals.DURATION] = message.note

        total_time += message.time
    if total_time % globals.DURATION == 0:
        notes_list[-1] = final_note
    return notes_list


def compute_consonant_chords(tonic):
    """
    Computes consonant chords for the given tonic in major key using the music formulas.

    :param tonic: the given tonic
    :return: None
    """
    globals.CONSONANT_CHORDS = [Chord(tonic % 12, globals.MAJOR_TRIAD),
                                Chord((tonic + 5) % 12, globals.MAJOR_TRIAD),
                                Chord((tonic + 7) % 12, globals.MAJOR_TRIAD),
                                Chord((tonic + 9) % 12, globals.MINOR_TRIAD),
                                Chord((tonic + 2) % 12, globals.MINOR_TRIAD),
                                Chord((tonic + 4) % 12, globals.MINOR_TRIAD),
                                Chord((tonic + 11) % 12, globals.DIM_CHORD)]


def get_velocity(midi_file):
    """
    Computes the velocity for the given song.

    :param midi_file: the given song
    :return: velocity of the given song
    """
    note_number, velocity = 0, 0

    for message in filter(lambda x: type(x) is Message, midi_file.tracks[1]):
        if message.type == 'note_on':
            note_number += 1
            velocity += message.velocity
    return int(velocity / note_number * 0.9)


def get_offset(midi_file):
    """
    Computes the offset for the given song.

    :param midi_file: the given song
    :return: offset of the given song
    """
    note_number, octave = 0, 0

    for message in filter(lambda x: type(x) is Message, midi_file.tracks[1]):
        if message.type == 'note_on':
            note_number += 1
            octave += int(message.note / 12)
    return 12 * (int(octave / note_number) - 1)


def write_output_chords(midi_file, tracks, output_chords, input_file, output_number):
    """
    Writes output chords to the given song.

    :param midi_file: the given song
    :param tracks: new tracks to add
    :param output_chords: computed chords to add
    :param input_file: input file name
    :param output_number: number of the output
    :return: None
    """
    velocity, offset = get_velocity(midi_file), get_offset(midi_file)

    for chord in output_chords:
        for i in range(3):
            tracks.append(
                Message('note_on', channel=0, note=chord.notes[i] + offset, velocity=velocity, time=0))
        tracks.append(Message('note_off', channel=0, note=chord.notes[0] + offset, velocity=velocity,
                              time=globals.DURATION))
        for i in range(1, 3):
            tracks.append(
                Message('note_off', channel=0, note=chord.notes[i] + offset, velocity=velocity, time=0))

    midi_file.tracks.append(tracks)

    key = get_key(input_file)
    print(f"The key of the melody in the file №{output_number + 1} is {key}")
    output_file = f"VladimirRyabenkoOutput{output_number + 1}-{key}.mid"""
    midi_file.save(output_file)
