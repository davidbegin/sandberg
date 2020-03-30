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

from sandberg.waitstaff import Waitstaff

# Add some weights to these, to favor certain rhythm
# This how we create genres
# TODO: War Rhythm
CHORD_RHYTHMS = [[4, 4, 4, 4], [4, 3, 4, 5], [8, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8]]
# CHORD_RHYTHMS = [[8, 8, 8, 8, 8, 8, 8, 8]]
# CHORD_RHYTHMS = [[4,4,4,4]]

INSTRUMENT_OCTAVE = {
    "Timpani": 2,
    "Ocarina": 5,
    "Shakuhachi": 5,
    "Synth Bass 1": 2,
    "Electric Guitar (jazz)": 2,
    "Tuba": 2,
    "Distortion Guitar": 1,
    "Overdriven Guitar": 2,
    "Slap Bass 2": 2,
}


def track_creator(instrument_name, channel):
    instrument = MidiInstrument()
    track = Track(instrument, channel=channel)
    instrument.name = instrument_name
    track.instrument.instrument_nr = MidiInstrument.names.index(instrument_name)
    return track


def midi_file_name(instrument_name):
    nice_inst = re.sub(r"[\s+()]", "", instrument_name).lower()
    # path = Path(__file__).parent.parent.joinpath("midi_file")
    # path = Path(__file__).parent.parent.joinpath(f"midi_files/test.mid")
    return Path(__file__).parent.parent.joinpath(f"midi_files/{nice_inst}.mid")


# A#, D#, G#
def generate_midi(
    *, instrument, chord_progression, pad, key="C", bpm=120, octave=None, applause=False
):
    composition = Composition()

    how_many_bars = 16

    # Make all these configurable
    # Or make them all random from a range
    track = Track(instrument, channel=1)

    drone_track = track_creator(pad, channel=2)
    # drone_track = track_creator("Pad4 (choir)", channel=2)

    # It's one of the few pitched drums
    timpani_track = track_creator("Timpani", channel=3)

    applause_track = track_creator("Applause", channel=4)

    bar = Bar(key, (4, 4))
    nc = NoteContainer("C", octave=2)
    bar.place_notes(nc, 1)
    applause_track.add_bar(bar)

    for _ in range(how_many_bars):

        # Can we get an index
        # We can with enumerate, but why do we want it
        for chord in chord_progression:
            # The Chord Progression

            bar = Bar(key, (4, 4))
            if not octave:
                octave = INSTRUMENT_OCTAVE.get(instrument.name, 4)

            for length in random.sample(CHORD_RHYTHMS, 1)[0]:
                some_notes = random.sample(chord, random.randint(1, len(chord)))
                nc = NoteContainer(some_notes, octave=int(octave))
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

    composition.add_track(timpani_track, channel=5)
    composition.add_track(drone_track)
    composition.add_track(track)

    # Do we want to add the channel when adding or creating the track?
    if applause:
        composition.add_track(applause_track)

    instrument_name = MidiInstrument.names[instrument.instrument_nr]
    write_Composition(midi_file_name(instrument_name), composition, bpm=bpm)
