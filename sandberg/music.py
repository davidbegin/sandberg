import os
import random

import roman
from mingus.containers.instrument import MidiInstrument

from sandberg.waitstaff import Waitstaff


def convert_roots_to_chord_chart(roots, scale_notes):
    return [roman.toRoman(scale_notes.index(root) + 1) for root in roots]


def print_instrument_options():
    print(MidiInstrument.names)


def find_pad():
    pass


def find_instrument(instrument, instrument_group):
    if instrument:
        try:
            instrument_nr = MidiInstrument.names.index(instrument)
        except ValueError:
            instrument_nr = int(instrument)
    elif instrument_group:
        # Choose a random from the instrument_group
        instrument = Waitstaff.choose_from_group(instrument_group)
        instrument_nr = MidiInstrument.names.index(instrument)
    else:
        instrument_nr = random.randint(0, len(MidiInstrument.names))

    midi_instrument = MidiInstrument()
    midi_instrument.name = MidiInstrument.names[instrument_nr]
    midi_instrument.instrument_nr = instrument_nr

    return midi_instrument
