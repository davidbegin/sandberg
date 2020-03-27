import argparse
import os

import mingus.core.chords as chords
import mingus.core.progressions as progressions

from sandberg.load_chords import load_chord_progression
from sandberg.generate_chords import generate_progression, expand_progression
from sandberg.music import find_instrument
from sandberg.midi_maker import generate_midi
from sandberg.waitstaff import Waitstaff


def chord_symbol(chord):
    return chords.determine(chord, shorthand=True)[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sandberg Options")

    parser.add_argument(
        "--key", "-k", dest="key", help="The Root Note to use for the song"
    )
    parser.add_argument(
        "--scale",
        "-s",
        dest="scale",
        default="Major",
        help="The scale to use for the song. Ex: Major, NaturalMinor, Locrian, Lydian",
    )
    parser.add_argument(
        "--minor",
        "-m",
        dest="minor",
        action="store_true",
        default=False,
        help="Whether to generate a minor progression",
    )
    parser.add_argument(
        "--instrument-group",
        "-g",
        dest="instrument_group",
        help="The instrument group to choose a random instrument from. Example: Guitar or Goofs",
    )
    parser.add_argument(
        "--instrument",
        "-i",
        dest="instrument",
        help="The instrument to use for the song. Example: Ocarina or 79",
    )
    # "1,4,5"
    # "I,II,IV,V"
    parser.add_argument(
        "--chord-progression",
        dest="chord_progression",
        help="A str of a chord progression you want to use. Ex: I,IV,V",
    )
    parser.add_argument(
        "--repeat-last-progression",
        "-r",
        dest="repeat_progression",
        action="store_true",
        default=False,
        help="A CSV file of a chord progression you want to use",
    )
    parser.add_argument(
        "--octave", "-o", dest="octave", help="The octave to use for the instrument"
    )
    parser.add_argument(
        "--random-instrument",
        dest="random_instrument",
        action="store_true",
        default=True,
        help="Choose a Random instrument to use for the song",
    )
    parser.add_argument(
        "--applause",
        "-a",
        dest="applause",
        action="store_true",
        default=False,
        help="Whether to celebrate",
    )
    parser.add_argument(
        "--choices",
        "-c",
        dest="show_choices",
        action="store_true",
        default=False,
        help="Display some instrument choices",
    )

    # We need to take a scale
    # We need to take BPM
    # We need to take in a chord-progression from the command line

    args = parser.parse_args()

    if args.show_choices:
        Waitstaff.show_choices()
        exit()
    # python music.py --chord-progression "1,2,4,5" --key C
    elif args.chord_progression:
        key, scale, chord_progression = expand_progression(args.chord_progression)
    elif args.repeat_progression:
        key, scale, chord_progression = load_chord_progression(
            "song", key=args.key, scale=args.scale
        )
    else:
        key, scale, chord_progression = generate_progression(
            key=args.key, scale=args.scale, minor=args.minor
        )

    chord_chart = [chord_symbol(chord) for chord in chord_progression]
    roman_chords = [
        progressions.determine(chord, key, True)[0] for chord in chord_progression
    ]

    instrument = find_instrument(args.instrument, args.instrument_group)

    generate_midi(
        instrument, key, chord_progression, octave=args.octave, applause=args.applause
    )

    if args.minor:
        key = chord_chart[0]
        scale = "Minor"

    os.system("clear")
    print(f"\n\t\t\033[4mSandberg Hit Writing Bot\033[0m")
    print(f"\n\t\tInstrument: {instrument.name} - {instrument.instrument_nr}")
    print(f"\nKey: {key}")
    print(f"\nScale: {scale}")
    print(f"\nChords: {' - '.join(chord_chart)}")
    print(f"\nChords: {' - '.join(roman_chords)}")

    print("\n")
