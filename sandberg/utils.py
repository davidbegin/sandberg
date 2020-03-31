import random

import mingus.core.notes as notes
from mingus.containers.note import Note


def key_finder():
    key = notes.int_to_note(random.randint(0, 11))
    if key in ["A#", "D#", "G#", "B#"]:
        return "C"
        note = Note(key)
        note.remove_redundant_accidentals()
        return note
    else:
        return key
