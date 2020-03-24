import csv
import mingus.core.scales as scales
import mingus.core.scales as scales
import mingus.core.progressions as progressions

from sandberg.music import convert_roots_to_chord_chart
from sandberg.utils import key_finder


# TODO: key
def load_chord_progression(chord_progression_file_name, key=None, scale="Major"):
    if not key:
        key = key_finder()

    with open(f"songs/{chord_progression_file_name}.csv") as csvfile:
        reader = csv.reader(csvfile)
        chord_progression_nums = list(reader)[0]

        scale_notes = scales.Major(key).ascending()
        # scale_notes = scales.NaturalMinor(key).ascending()

        song = [scale_notes[int(chord_num) - 1] for chord_num in chord_progression_nums]
        chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
        chord_progression = progressions.to_chords(chord_chart, key)
    return key, scale, chord_progression
