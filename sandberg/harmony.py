from itertools import cycle

import roman


def substitute_major_for_minor(chord_chart):
    minor_chords = []
    for chord in chord_chart:
        num = roman.fromRoman(chord)
        new_num = num - 2
        if new_num < 1:
            new_num = new_num + 7
        minor_chords.append(roman.toRoman(new_num))
    return minor_chords
