class Chord(object):
    def __init__(self, base_note, chord_type):
        self.base_note = base_note
        self.type = chord_type
        self.note_list = [(base_note + note) % 12 for note in chord_type]

    def has_note(self, note):
        if note is None:
            return False
        for chord_note in self.note_list:
            if chord_note == note % 12:
                return True
        return False

    def __eq__(self, other):
        return self.base_note == other.base_note and self.type == other.type
