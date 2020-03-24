import random

import os

import roman

from mingus.containers.instrument import MidiInstrument

def convert_roots_to_chord_chart(roots, scale_notes):
    return [roman.toRoman(scale_notes.index(root) + 1) for root in roots]

def find_instrument(args):
    # print(MidiInstrument.names)

    if args.random_instrument:
        instrument_nr = random.randint(0, len(MidiInstrument.names))
        instrument_nr = 40
    else:
        instrument_nr = MidiInstrument.names.index(args.instrument)

    instrument = MidiInstrument()
    instrument_name = MidiInstrument.names[instrument_nr]
    instrument.instrument_nr = instrument_nr
    print(f"Instrument: {MidiInstrument.names[instrument_nr]}")
    print(f"Instrument: {len(MidiInstrument.names)}")

    return instrument
