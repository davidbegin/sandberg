import csv
import mingus.core.scales as scales


def load_chord_progression(chord_progression_file_name):
    key = chord_progression_file_name.split("-")[0]

    with open(f"songs/{chord_progression_file_name}.csv") as csvfile:
        reader = csv.reader(csvfile)
        chord_progression_nums = list(reader)[0]

        scale_notes = scales.NaturalMinor(key).ascending()
        song = [scale_notes[int(chord_num) - 1] for chord_num in chord_progression_nums]
        chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
        #
        chord_progression = progressions.to_chords(chord_chart, key + "m")
    return key, chord_progression
