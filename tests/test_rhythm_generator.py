import random

import pytest

from sandberg.rhythm_generator import choose_rhythm, generate_rhythm, split_note, split_bar

def test_choose_rhythm():
    random.seed(0)
    rhythm = choose_rhythm((4,4))
    assert rhythm == [8, 4, 8, 8, 4, 8]

def test_generate_rhythm():
    rhythm = generate_rhythm()
    # breakpoint()
    # print("")
    ## assert rhythm

def test_split_note():
    result = split_note(4)
    assert result == [8,8]
    result = split_note(8)
    assert result == [16,16]

def test_split_bar():
    result = split_bar([4])
    assert result == [8,8]


# dotted-note = take half length of the note and add it to yourself
def test_split_note_dotted():
    result = split_not_dotted(4)
    assert result == [6,8]
