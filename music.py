import argparse

import mingus.core.chords as chords

from sandberg.load_chords import load_chord_progression
from sandberg.generate_chords import generate_progression
from sandberg.music import find_instrument
from sandberg.midi_maker import generate_midi


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
        "--instrument",
        dest="instrument",
        default="Ocarina",
        help="The instrument to use for the song",
    )
    parser.add_argument(
        "--chord-progression",
        dest="chord_progression",
        help="A CSV file of a chord progression you want to use",
    )
    parser.add_argument(
        "--random-instrument",
        dest="random_instrument",
        action="store_true",
        default=True,
        help="Choose a Random instrument to use for the song",
    )

    # We need to take a scale
    # We need to take BPM
    # We need to take in a chord-progression from the command line

    args = parser.parse_args()

    # python music.py --chord-progression "1,2,4,5" --key C

    # We could also specify it all from the command line
    if args.chord_progression:
        key, chord_progression = load_chord_progression(args.chord_progression)
    else:
        # This needs to take in the key and scale
        key, scale, chord_progression = generate_progression(
            key=args.key, scale=args.scale
        )

    chord_chart = [chord_symbol(chord) for chord in chord_progression]

    instrument = find_instrument(args)

    print(f"Key: {key}")
    print(f"Scale: {scale}")
    print(f"Chord Chart: {' - '.join(chord_chart)}")
    print("\n")
