import music21
from mido import Message, MetaMessage

import globals
from chord import Chord


def get_average_velocity(mid):
    note_count, avg_velocity = 0, 0

    for message in mid.tracks[1]:
        if isinstance(message, Message) and message.type == 'note_on':
            avg_velocity += message.velocity
            note_count += 1
    return int(avg_velocity / note_count)


def get_average_octave(mid):
    note_count, avg_octave = 0, 0

    for message in mid.tracks[1]:
        if isinstance(message, Message) and (message.type == 'note_on'):
            avg_octave += int(message.note / 12)
            note_count += 1
    return int(avg_octave / note_count)


def get_notes_amount(track):
    beats = 0

    for message in track:
        if type(message) is Message:
            beats += message.time
    length = (beats + globals.DURATION - 1) // globals.DURATION
    return length


def get_tempo(mid):
    tempo = 0

    for track in mid.tracks:
        for message in track:
            if isinstance(message, MetaMessage) and message.type == "set_tempo":
                tempo = message.tempo
    return tempo


def determine_notes(track):
    length = get_notes_amount(track)
    notes_list = [None] * length
    beats, last_note = 0, 0

    for message in track:
        if type(message) is Message:
            if beats % globals.DURATION == 0 and message.type == "note_on":
                if notes_list[beats // globals.DURATION] is None:
                    notes_list[beats // globals.DURATION] = message.note

            if message.type == "note_off":
                last_note = message.note

            beats += message.time
    if beats % globals.DURATION == 0:
        notes_list[-1] = last_note
    return notes_list


def identify_music_scale():
    score = music21.converter.parse(globals.INPUT_FILE_NAME)
    key = score.analyze('key')

    if key.mode == "minor":
        globals.SCALE = (key.tonic.midi + 3) % 12
    else:
        globals.SCALE = key.tonic.midi % 12


def compute_consonant_chords():
    globals.CONSONANT_CHORDS = [Chord(globals.SCALE % 12, globals.MAJOR_TRIAD),
                                Chord((globals.SCALE + 5) % 12, globals.MAJOR_TRIAD),
                                Chord((globals.SCALE + 7) % 12, globals.MAJOR_TRIAD),
                                Chord((globals.SCALE + 9) % 12, globals.MINOR_TRIAD),
                                Chord((globals.SCALE + 2) % 12, globals.MINOR_TRIAD),
                                Chord((globals.SCALE + 4) % 12, globals.MINOR_TRIAD),
                                Chord((globals.SCALE + 11) % 12, globals.DIM_CHORD)]


def write_output_chords(mid, tracks, output_chords):
    velocity = int(get_average_velocity(mid) * 0.9)
    average_displacement = 12 * (get_average_octave(mid) - 1)

    for chord in output_chords:
        tracks.append(
            Message('note_on', channel=0, note=chord.note_list[0] + average_displacement, velocity=velocity, time=0))
        tracks.append(
            Message('note_on', channel=0, note=chord.note_list[1] + average_displacement, velocity=velocity, time=0))
        tracks.append(
            Message('note_on', channel=0, note=chord.note_list[2] + average_displacement, velocity=velocity, time=0))
        tracks.append(Message('note_off', channel=0, note=chord.note_list[0] + average_displacement, velocity=velocity,
                              time=globals.DURATION))
        tracks.append(
            Message('note_off', channel=0, note=chord.note_list[1] + average_displacement, velocity=velocity, time=0))
        tracks.append(
            Message('note_off', channel=0, note=chord.note_list[2] + average_displacement, velocity=velocity, time=0))

    mid.tracks.append(tracks)
    mid.save(globals.OUTPUT_FILE_NAME)
