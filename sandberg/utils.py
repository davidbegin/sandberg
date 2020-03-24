import random

import mingus.core.notes as notes


def key_finder():
    return notes.int_to_note(random.randint(0, 11))
