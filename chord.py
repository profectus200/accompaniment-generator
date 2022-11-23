"""Implements the 'Chord' class."""


class Chord(object):
    """
    Represents a chord.

    :argument base_note: root note of the chord
    :argument note_list: notes in the chord
    """

    def __init__(self, base_note, chord_type):
        """
        Standard constructor.

        :param base_note: root note of the chord
        """
        self.base_note = base_note
        self.note_list = [(base_note + note) % 12 for note in chord_type]

    def is_note_in_chord(self, note):
        """
        Checks if the chord has the given note.

        :param note: the given note.
        :return: true if the chord has the given note and false otherwise
        """
        if note is not None and note % 12 in self.note_list:
            return True
        return False

    def __eq__(self, other):
        """
        Checks whether two chords are equal.

        :param other: other chord to compare
        :return: true if two chords are equal and false otherwise
        """
        return self.note_list == other.note_list
