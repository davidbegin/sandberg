import random
import re
from pathlib import Path

from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Composition
from mingus.containers.instrument import MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi.midi_file_out import MidiFile as MidiFileOut
from mingus.midi.midi_file_out import write_Composition
from mingus.containers.note_container import NoteContainer

# Add some weights to these, to favor certain rhythm
# This how we create genres
# TODO: War Rhytmn
# CHORD_RHYTHMS = [[4, 4, 4, 4], [4, 3, 4, 5], [8, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8]]
CHORD_RHYTHMS = [[8, 8, 8, 8, 8, 8, 8, 8]]
# CHORD_RHYTHMS = [[4,4,4,4]]

INSTRUMENT_OCTAVE = {
    "Timpani": 2,
    "Ocarina": 5,
    "Shakuhachi": 5,
    "Synth Bass 1": 2,
    "Electric Guitar (jazz)": 2,
    "Tuba": 2,
}


def track_creator(instrument_name):
    instrument = MidiInstrument()
    track = Track(instrument)
    instrument.name = instrument_name
    track.instrument.instrument_nr = MidiInstrument.names.index(instrument_name)
    return track


def generate_midi(instrument, key, chord_progression, octave=None, applause=False):
    composition = Composition()

    how_many_bars = 16

    # When is the instrument_nr used in the mingus library
    # to actually choose an instrument in the midi file

    drone_track = track_creator("Pad4 (choir)")

    timpani_track = track_creator("Timpani")

    applause_track = track_creator("Applause")

    track = Track(instrument)

    bar = Bar(key, (4, 4))
    nc = NoteContainer("C", octave=2)
    bar.place_notes(nc, 1)
    applause_track.add_bar(bar)

    for _ in range(how_many_bars):

        for chord in chord_progression:
            # The Chord Progression

            bar = Bar(key, (4, 4))
            if not octave:
                octave = INSTRUMENT_OCTAVE.get(instrument.name, 4)
            nc = NoteContainer(chord, octave=int(octave))
            for length in random.sample(CHORD_RHYTHMS, 1)[0]:
                bar.place_notes(nc, length)
            track.add_bar(bar)

            drone_bar = Bar(key, (4, 4))
            nc = NoteContainer(chord[0], octave=2)
            drone_bar.place_notes(nc, 1)
            drone_track.add_bar(drone_bar)

            timpani_bar = Bar(key, (4, 4))
            nc = NoteContainer(key, octave=2)
            for length in [4, 4, 4, 4]:
                timpani_bar.place_notes(nc, length)
            timpani_track.add_bar(timpani_bar)

    # Which track we add first

    composition.add_track(timpani_track)
    composition.add_track(drone_track)

    if applause:
        composition.add_track(applause_track)

    composition.add_track(track)

    instrument_name = MidiInstrument.names[instrument.instrument_nr]

    nice_inst = re.sub(r"[\s+()]", "", instrument_name).lower()
    # path = Path(__file__).parent.parent.joinpath("midi_file")
    # path = Path(__file__).parent.parent.joinpath(f"midi_files/test.mid")
    path = Path(__file__).parent.parent.joinpath(f"midi_files/{nice_inst}.mid")

    write_Composition(path, composition)


# def old_generate_midi(instrument, key, chord_progression):
#     composition = Composition()
#     how_many_bars = 16

#     drums = MidiPercussionInstrument()
#     drums_instrument = MidiInstrument()
#     # drums_instrument.instrument_nr = 115
#     # drums.instrPument_nr = random.randint(0, len(drums.mapping.keys()))
#     drum_track = Track(drums_instrument)
#     track = Track(instrument)

#     for _ in range(how_many_bars):
#         # instrument.instrument_nr = 115
#         bar = Bar(key, (4, 4))
#         hc = NoteContainer([key])
#         for length in [4, 4, 4, 4]:
#             bar.place_notes(hc, length)
#         drum_track.add_bar(bar)

#         for chord in chord_progression:
#             bar = Bar(key, (4, 4))
#             nc = NoteContainer(chord)
#             for length in random.sample(CHORD_RHYTHMS, 1)[0]:
#                 bar.place_notes(nc, length)
#             track.add_bar(bar)

#     # These end up as the same instrument
#     composition.add_track(drum_track)
#     composition.add_track(track)

#     path = Path(__file__).parent.parent.joinpath("midi_files/test.mid")
#     write_Composition(path, composition)
