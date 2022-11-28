"""Implements the 'Chord' class."""


class Chord(object):
    """
    Represents a chord.

    :argument base_note: root note of the chord
    :argument notes: notes in the chord
    """

    def __init__(self, base_note, triad):
        """
        Standard constructor.

        :param base_note: root note of the chord
        :param triad: triad of notes which form a chord of the special type
        """
        self.base_note = base_note
        self.notes = [(base_note + note) % 12 for note in triad]

    def is_note_in_chord(self, note):
        """
        Checks if the chord has the given note.

        :param note: the given note.
        :return: true if the chord has the given note and false otherwise
        """
        if note is not None and note % 12 in self.notes:
            return True
        return False

    def __eq__(self, other):
        """
        Checks whether two chords are equal.

        :param other: other chord to compare
        :return: true if two chords are equal and false otherwise
        """
        return self.notes == other.notes
