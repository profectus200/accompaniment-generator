"""Implements the 'Chord' class."""


class Chord(object):
    """
    Represents a chord.

    :argument root_note: root note of the chord
    :argument type: type of the chord
    :argument note_list: notes in the chord
    """

    def __init__(self, root_note, chord_type):
        """
        Standard constructor.

        :param root_note: root note of the chord
        :param chord_type: type of the chord
        """
        self.root_note = root_note
        self.type = chord_type
        self.note_list = [(root_note + note) % 12 for note in chord_type]

    def has_note(self, note):
        """
        Checks if the chord has the given note.

        :param note: the given note.
        :return: true if the chord has the given note and false otherwise
        """
        if note is None:
            return False
        if note % 12 in self.note_list:
            return True
        return False

    def __eq__(self, other):
        """
        Checks whether two chords are equal.

        :param other: other chord to compare
        :return: true if two chords are equal and false otherwise
        """
        return self.root_note == other.root_note and self.type == other.type
