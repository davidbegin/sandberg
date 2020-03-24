import csv
import random

import roman

import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.progressions as progressions

from sandberg.music import convert_roots_to_chord_chart


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


def generate_progression():
    # Root Notes
    song = []
    key_int = random.randint(0, 11)
    key = notes.int_to_note(key_int)
    # scale       = scales.Diatonic(key, (3,7))
    scale = scales.NaturalMinor(key)
    scale_notes = scale.ascending()
    song.append(key)

    print(f"I: {key}")
    # Getting the 2nd
    next_chord, next_chord_int = progress(scale_notes, 1, 2)
    song.append(next_chord)

    while True:
        next_chord, next_chord_int = progress(
            scale_notes, next_chord_int, len(song) + 1
        )
        song.append(next_chord)
        if len(song) % 4 == 0 and next_chord_int in [1, 6]:
            break

    chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
    chord_chart_2 = [
        progressions.substitute_major_for_minor(chord[0], 0)[0] for chord in chord_chart
    ]
    chord_progression = progressions.to_chords(chord_chart_2, key)

    chord_progression_nums = [scale_notes.index(note) + 1 for note in song]

    song_file_name = f"{key}-{len(song)}"
    with open(f"songs/{song_file_name}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(chord_progression_nums)

    return key, chord_progression


def progress(scale_notes, chord_position, bar_position):
    start_of_bar = range(1, 1000, 4)

    next_chord_int = random.choice(CLASSICAL_HARMONY[chord_position])
    next_chord = scale_notes[next_chord_int - 1]

    # 1  Chord not on the top of a 4 bar measure
    if next_chord_int == 1 and bar_position not in start_of_bar:
        progress(scale_notes, chord_position, bar_position)

    print(f"{roman_chord_fmt(next_chord_int)}: {chord_fmt(next_chord, next_chord_int)}")
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

