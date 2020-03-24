import random
from pathlib import Path

from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers import Composition
from mingus.containers.instrument import MidiInstrument
from mingus.containers.instrument import MidiPercussionInstrument
from mingus.midi.midi_file_out import MidiFile as MidiFileOut

# from mingus.midi.midi_file_out import write_NoteContainer
# from mingus.midi.midi_file_out import write_Bar
# from mingus.midi.midi_file_out import write_Track

from mingus.midi.midi_file_out import write_Composition
from mingus.containers.note_container import NoteContainer

# Add some weights to these, to favor certain rhythm
# This how we create genres
CHORD_RHYTHMS = [[4, 4, 4, 4], [4, 3, 4, 5], [8, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8]]


def generate_midi(instrument, key, chord_progression):
    composition = Composition()

    how_many_bars = 16
    track = Track(instrument)
    for _ in range(how_many_bars):
        for chord in chord_progression:
            bar = Bar(key, (4, 4))
            nc = NoteContainer(chord)
            for length in random.sample(CHORD_RHYTHMS, 1)[0]:
                bar.place_notes(nc, length)
            track.add_bar(bar)

    composition.add_track(track)
    path = Path(__file__).parent.parent.joinpath("midi_files/test.mid")
    write_Composition(path, composition)


def new_generate_midi(instrument, key, chord_progression):
    composition = Composition()
    how_many_bars = 16

    drums = MidiPercussionInstrument()
    drums_instrument = MidiInstrument()
    # drums_instrument.instrument_nr = 115
    # drums.instrPument_nr = random.randint(0, len(drums.mapping.keys()))
    drum_track = Track(drums_instrument)
    track = Track(instrument)

    for _ in range(how_many_bars):
        # instrument.instrument_nr = 115
        bar = Bar(key, (4, 4))
        hc = NoteContainer([key])
        for length in [4, 4, 4, 4]:
            bar.place_notes(hc, length)
        drum_track.add_bar(bar)

        for chord in chord_progression:
            bar = Bar(key, (4, 4))
            nc = NoteContainer(chord)
            for length in random.sample(CHORD_RHYTHMS, 1)[0]:
                bar.place_notes(nc, length)
            track.add_bar(bar)

    # These end up as the same instrument
    composition.add_track(drum_track)
    composition.add_track(track)

    path = Path(__file__).parent.parent.joinpath("midi_files/test.mid")
    write_Composition(path, composition)
