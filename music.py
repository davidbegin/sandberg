import random
import os
import argparse
import csv

import roman
import mingus.core.progressions as progressions
import mingus.core.chords as chords
import mingus.core.notes as notes
import mingus.core.scales as scales
from mingus.containers.note_container import NoteContainer
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers.instrument import MidiInstrument


from mingus.midi.midi_file_out import MidiFile as MidiFileOut
from mingus.midi.midi_file_out import write_NoteContainer
from mingus.midi.midi_file_out import write_Bar
from mingus.midi.midi_file_out import write_Track



def convert_roots_to_chord_chart(roots, scale_notes):
    return [
        roman.toRoman(scale_notes.index(root) + 1) for root in roots
    ]

# Fux / Bach Rules 
CLASSICAL_HARMONY = {
        1: [2, 3, 4, 5, 6, 7],
        2: [5, 7, 1],
        3: [6, 4],
        4: [2, 5, 7, 1],
        5: [1, 6],
        6: [4, 2],
        7: [1, 6]
}

# Add some weights to these, to favor certain rhythm
# This how we create genres
CHORD_RHYTHMS = [
        [4, 4, 4, 4],
        [4, 3, 4, 5],
        [8, 8, 4, 4, 4]
]


def roman_chord_fmt(chord_position):
    rome = f"{roman.toRoman(chord_position)}"
    if chord_position not in [1,4,5]:
        return rome.lower()
    return rome


def chord_fmt(chord, chord_position):
    if chord_position == 7:
        return f"{chord}dim"
    elif chord_position not in [1,4,5]:
        return f"{chord}m"
    return chord



def progress(scale_notes, chord_position, bar_position):
    start_of_bar = range(1, 1000, 4)

    next_chord_int = random.choice(CLASSICAL_HARMONY[chord_position])
    next_chord = scale_notes[next_chord_int - 1]

    # 1  Chord not on the top of a 4 bar measure
    if next_chord_int == 1 and bar_position not in start_of_bar:
        progress(scale_notes, chord_position, bar_position)

    print(f"{roman_chord_fmt(next_chord_int)}: {chord_fmt(next_chord, next_chord_int)}")
    return next_chord, next_chord_int

def generate_progression():
    # Root Notes
    song = [ ]
    key_int     = random.randint(0,11)
    key         = notes.int_to_note(key_int)
    scale       = scales.Diatonic(key, (3,7))
    scale_notes = scale.ascending()
    song.append(key)

    print(f"I: {key}")
    # Getting the 2nd
    next_chord, next_chord_int = progress(scale_notes, 1, 2)
    song.append(next_chord)

    while True:
        next_chord, next_chord_int = progress(scale_notes, next_chord_int, len(song) + 1)
        song.append(next_chord)
        if len(song) % 4 == 0 and next_chord_int in [1, 6]:
            break

    chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
    chord_progression = progressions.to_chords(chord_chart, key) 
    chord_progression_nums = [ scale_notes.index(note) + 1 for note in song ]

    song_file_name = f"{key}-{instrument_name.lower().replace(' ', '_')}-{len(song)}"
    with open(f'songs/{song_file_name}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(chord_progression_nums)

    return key, chord_progression


def load_chord_progression(chord_progression_file_name):
    key = chord_progression_file_name.split("-")[0]

    with open(f'songs/{chord_progression_file_name}.csv') as csvfile:
        reader = csv.reader(csvfile)
        chord_progression_nums = list(reader)[0]

        scale_notes = scales.Diatonic(key, (3,7)).ascending()
        song = [ scale_notes[int(chord_num) - 1] for chord_num in chord_progression_nums ]
        chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
        chord_progression = progressions.to_chords(chord_chart, key) 
    return key, chord_progression

    

def generate_midi(key, chord_progression):
    track = Track(instrument)
    # Can't handle Sharp keys for some reason
    how_many_bars = 16
    for _ in range(how_many_bars):
        for chord in chord_progression:
            bar = Bar(key, (4, 4))
            nc = NoteContainer(chord)

            for length in random.sample(CHORD_RHYTHMS, 1)[0]:
                bar.place_notes(nc, length)
            track.add_bar(bar)

    write_Track("midi_files/test.mid", track, bpm=120)

# We need minor
if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description="Sandberg Options")

    parser.add_argument('--instrument', dest="instrument",
            default="Ocarina", help='The instrument to use for the song')
    parser.add_argument('--chord-progression', dest="chord_progression",
            help='A CSV file of a chord progression you want to use')
    parser.add_argument('--random-instrument', dest="random_instrument",
            action="store_true",
            default=False, help='Choose a Random instrument to use for the song')

    args = parser.parse_args()

    print(MidiInstrument.names)

    if args.random_instrument:
        instrument_nr = random.randint(0, len(MidiInstrument.names))
    else:
        instrument_nr = MidiInstrument.names.index(args.instrument)

    instrument = MidiInstrument()
    instrument_name = MidiInstrument.names[instrument_nr]
    instrument.instrument_nr = instrument_nr
    print(f"Instrument: {MidiInstrument.names[instrument_nr]}")

    # pylang: start on the I and end on the II = new age music
    if args.chord_progression:
        key, chord_progression = load_chord_progression(args.chord_progression)
    else:
        key, chord_progression = generate_progression()

    generate_midi(key, chord_progression)


