import argparse
import requests
import os
import re

import mingus.core.chords as chords
import mingus.core.progressions as progressions

from sandberg.load_chords import load_chord_progression
from sandberg.generate_chords import generate_progression, expand_progression
from sandberg.music import find_instrument
from sandberg.midi_maker import generate_midi
from sandberg.waitstaff import Waitstaff


def chord_symbol(chord):
    return chords.determine(chord, shorthand=True)[0]


# What are the multiple ways to break copywrite
#
# How much content needs to be there for copyright
# more than 7 notes in Rhythm
# frenck: Hmm... just because something is copyrighted, it doesn't mean you
# cannot use it right?
# Fair-use
#
# transformative things to the content
# how much do you have to change
# frenck: @beginbot No I cannot... since I'm licensed
#
# License to Stream
# hazeanderson: BMI, ASCAP or Seacac
# hazeanderson: SEASAC :D
# *spfar:* beginbot is back!
# artmattdank: perchance to Stream
def lawyer_up():
    # Find Chord progression
    # curl "https://www.guitarplayerbox.com/song/list/containing/chords/?chSel=A&chSel=Bm&chSel=Fsharpm&maxCapo=5" | grep songNameLabel | sed 's/.*[0-9]\">//g' | sed 's/<.*//g'^C
    url = "https://www.guitarplayerbox.com/song/list/containing/chords/?chSel=A&chSel=Bm&chSel=Fsharpm"
    # x = requests.get(url)
    # with open("copywrite_claims.html", "w+") as f:
    #     f.write(x.text)
    # song_search = re.compile("songNameLabel(.*)")
    # # We need to search in here
    # # breakpoint()
    # # songNameLabel


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sandberg Options")

    parser.add_argument(
        "--key", "-k", dest="key", help="The Root Note to use for the song"
    )
    parser.add_argument("--bpm", "-b", dest="bpm", help="Beats per minute", default=120)
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
    parser.add_argument(
        "--save-filename", dest="save_filename", help="Where to store the MIDI file",
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

    pad = Waitstaff.choose_from_group("Pad")
    instrument = find_instrument(args.instrument, args.instrument_group)

    # os.system("clear")
    print(f"\n\t\t\033[4mSandberg Hit Writing Bot\033[0m")
    print(f"\n\t\tInstrument: {instrument.name} - {instrument.instrument_nr}")
    print(f"\n\t\tPad: {pad}")
    print(f"\nKey: {key}")
    print(f"\nScale: {scale}")
    print(f"\nChords: {' - '.join(chord_chart)}")
    print(f"\nChords: {' - '.join(roman_chords)}")
    print("\n")

    if args.octave:
        octave = int(args.octave)
    else:
        octave = None

    generate_midi(
        applause=args.applause,
        bpm=int(args.bpm),
        chord_progression=chord_progression,
        instrument=instrument,
        key=key,
        octave=octave,
        pad=pad,
        save_filename=args.save_filename,
    )

    if args.minor:
        key = chord_chart[0]
        scale = "Minor"
