import os
import random

import roman
from mingus.containers.instrument import MidiInstrument


def convert_roots_to_chord_chart(roots, scale_notes):
    return [roman.toRoman(scale_notes.index(root) + 1) for root in roots]


def print_instrument_options():
    print(MidiInstrument.names)


def find_instrument(args):
    # print_instrument_options()
    instrument = MidiInstrument()

    if args.instrument:
        instrument_nr = MidiInstrument.names.index(args.instrument)
    elif args.random_instrument:
        instrument_nr = random.randint(0, len(MidiInstrument.names))

    instrument.instrument_nr = instrument_nr

    print(
        f"\n\n\tInstrument: {MidiInstrument.names[instrument_nr]} - {instrument_nr}\n"
    )

    return instrument
