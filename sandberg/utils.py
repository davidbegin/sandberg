import random

import mingus.core.notes as notes
from mingus.containers.note import Note


def key_finder():
    key_index = random.randint(0, 11)
    key = notes.int_to_note(key_index)

    if key in ["A#", "D#", "G#", "B#"]:
        return notes.int_to_note(key_index, "b")
    else:
        return key
