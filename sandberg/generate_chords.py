import csv
import random

import roman
import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.progressions as progressions

from sandberg.music import convert_roots_to_chord_chart
from sandberg.harmony import substitute_major_for_minor
from sandberg.utils import key_finder


# Fux / Bach Rules
CLASSICAL_HARMONY = {
    1: [2, 3, 4, 5, 6, 7],
    2: [5, 7, 1],
    3: [6, 4],
    4: [2, 5, 7, 1],
    5: [1, 6],
    6: [4, 2],
    7: [1, 6],
}


def expand_progression(chord_progression, key=None, scale="Major"):
    chord_chart = [chord.strip() for chord in chord_progression.split(",")]
    if key is None:
        key = key_finder()

    scale_notes, scale_name = scale_finder(key, scale_name=scale)
    chord_progression = progressions.to_chords(chord_chart, key)
    root_notes = [chord[0] for chord in chord_progression]
    chord_progression_nums = [scale_notes.index(note) + 1 for note in root_notes]
    save_song(key, chord_progression_nums)
    return key, scale, chord_progression


def generate_progression(key=None, scale=None, minor=False):
    root_notes = []
    if key is None:
        key = key_finder()

    scale_notes, scale_name = scale_finder(key, scale_name=scale)
    root_notes.append(key)

    next_chord, next_chord_int = progress(scale_notes, chord_position=1, bar_position=2)

    root_notes.append(next_chord)

    while True:
        next_chord, next_chord_int = progress(
            scale_notes,
            chord_position=next_chord_int,
            bar_position=(len(root_notes) + 1),
        )
        root_notes.append(next_chord)
        if len(root_notes) % 4 == 0 and next_chord_int in [1, 6]:
            break

    chord_chart = convert_roots_to_chord_chart(root_notes, scale_notes[:-1])

    if minor:
        chord_chart = substitute_major_for_minor(chord_chart)
        # Hmmmm Is the chord progression correct here

    chord_progression = progressions.to_chords(chord_chart, key)
    chord_progression_nums = [scale_notes.index(note) + 1 for note in root_notes]
    save_song(key, chord_progression_nums)
    return key, scale, chord_progression


# How can we name randomly generated chord progressions?
# How SHOULD we name randomly generated chord progressions?
def save_song(key, chord_progression_nums):
    length = len(chord_progression_nums)
    second_to_last = roman.toRoman(chord_progression_nums[-2])
    root_notes_file_name = f"song"
    # root_notes_file_name = f"{key}-{second_to_last}-{length}"

    with open(f"songs/{root_notes_file_name}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(chord_progression_nums)


def progress(scale_notes, *, chord_position, bar_position):
    start_of_bar = range(1, 1000, 4)

    next_chord_int = random.choice(CLASSICAL_HARMONY[chord_position])
    next_chord = scale_notes[next_chord_int - 1]

    # I Chord not on the top of a 4 bar measure
    if next_chord_int == 1 and bar_position not in start_of_bar:
        progress(scale_notes, chord_position=chord_position, bar_position=bar_position)

    return next_chord, next_chord_int


def roman_chord_fmt(chord_position):
    rome = f"{roman.toRoman(chord_position)}"
    if chord_position not in [1, 4, 5]:
        return rome.lower()
    return rome


def chord_fmt(chord, chord_position):
    if chord_position == 7:
        return f"{chord}dim"
    elif chord_position not in [1, 4, 5]:
        return f"{chord}m"
    return chord


# TODO: Move this to utils
def scale_finder(key, scale_name="Major"):
    def func_not_found(key):
        print(f"No Scale: {scale_name} Found!")
        return scales.Major(key)

    func = getattr(scales, scale_name, func_not_found)
    scale = func(key)
    return scale.ascending(), scale_name
