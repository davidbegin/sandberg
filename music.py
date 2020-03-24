import argparse

from sandberg.load_chords import load_chord_progression
from sandberg.generate_chords import generate_progression
from sandberg.music import find_instrument
from sandberg.midi_maker import generate_midi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sandberg Options")

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

    args = parser.parse_args()

    if args.chord_progression:
        key, chord_progression = load_chord_progression(args.chord_progression)
    else:
        key, chord_progression = generate_progression()

    instrument = find_instrument(args)

    generate_midi(instrument, key, chord_progression)
