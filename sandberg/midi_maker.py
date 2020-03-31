import random
from random import randint

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
from mingus.core.scales import Major, NaturalMinor

from sandberg.waitstaff import Waitstaff

# Add some weights to these, to favor certain rhythm
# This how we create genres
# TODO: War Rhythm
# CHORD_RHYTHMS = [
#     [4, 4, 4, 4],
#     [8, 8, 8, 8, 8, 8, 8, 8]
# ]
# ANGULAR_RHYTHMS = [
#     [8, 8, 4, 4, 4],
#     [8, 8, 8,8, 4, 4],
#     [8, 8, 8,8, 8,8, 4],
# ]
# CHORD_RHYTHMS = [[4, 4, 4, 4], [4, 3, 4, 5], [8, 8, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8]]
# CHORD_RHYTHMS = [[8, 8, 8, 8, 8, 8, 8, 8]]
# CHORD_RHYTHMS = [[4,4,4,4]]


CHORD_RHYTHMS = [
    {"rhythm": [4, 4, 4, 4], "weight": 2},
    {"rhythm": [8, 8, 4, 4, 4], "weight": 3},
    {"rhythm": [8, 8, 8, 8, 8, 8, 8, 8], "weight": 3},
    {"rhythm": [4, 8, 8, 8, 8, 8, 8], "weight": 3},
    {"rhythm": [4, 4, 8, 8, 8, 8], "weight": 3},
    {"rhythm": [8, 8, 8, 16, 16, 16, 16, 8, 8, 8], "weight": 3},
    {"rhythm": [8, 16, 16, 8, 16, 16, 16, 16, 8, 16, 16, 8], "weight": 3},
    {"rhythm": [2, 4, 4], "weight": 1},
]

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
    "Electric Bass (pick) ": 2,
}

INSTRUMENT_POLYPHONY = {"Ocarina": 1}


keyboards = [
    "Acoustic Grand Piano",
    "Bright Acoustic Piano",
    "Electric Grand Piano",
    "Honky-tonk Piano",
    "Electric Piano 1",
    "Electric Piano 2",
    "Harpsichord",
    "Clavi",
    "Celesta",
    "Glockenspiel",
    "Music Box",
    "Vibraphone",
    "Marimba",
    "Xylophone",
    "Tubular Bells",
    "Dulcimer",
    "Drawbar Organ",
    "Percussive Organ",
    "Rock Organ",
    "Church Organ",
    "Reed Organ",
    "Accordion",
    "Harmonica",
    "Tango Accordion",
]

guitars = [
    "Acoustic Guitar (nylon)",
    "Acoustic Guitar (steel)",
    "Electric Guitar (jazz)",
    "Electric Guitar (clean)",
    "Electric Guitar (muted)",
    "Overdriven Guitar",
    "Distortion Guitar",
    "Guitar harmonics",
]

# Basses
basses = [
    "Acoustic Bass",
    "Electric Bass (finger)",
    "Electric Bass (pick)",
    "Fretless Bass",
    "Slap Bass 1",
    "Slap Bass 2",
    "Synth Bass 1",
    "Synth Bass 2",
]

strings = [
    # Strings
    "Violin",
    "Viola",
    "Cello",
    "Contrabass",
    "Tremolo Strings",
    "Pizzicato Strings",
    "Orchestral Harp",
    "Timpani",
    "String Ensemble 1",
    "String Ensemble 2",
    "SynthStrings 1",
    "SynthStrings 2",
]


voices = [
    # Voices
    "Choir Aahs",
    "Voice Oohs",
    "Synth Voice",
]


orchestra = [
    # Orchestra
    "Orchestra Hit",
    "Trumpet",
    "Trombone",
    "Tuba",
    "Muted Trumpet",
    "French Horn",
    "Brass Section",
    "SynthBrass 1",
    "SynthBrass 2",
    "Soprano Sax",
    "Alto Sax",
    "Tenor Sax",
    "Baritone Sax",
    "Oboe",
    "English Horn",
    "Bassoon",
    "Clarinet",
    "Piccolo",
    "Flute",
]

wind_instruments = [
    # Wind Things
    "Recorder",
    "Pan Flute",
    "Blown Bottle",
    "Shakuhachi",
    "Whistle",
    "Ocarina",
]


leads = [
    # Leads
    "Lead1 (square)",
    "Lead2 (sawtooth)",
    "Lead3 (calliope)",
    "Lead4 (chiff)",
    "Lead5 (charang)",
    "Lead6 (voice)",
    "Lead7 (fifths)",
    "Lead8 (bass + lead)",
]


pads = [
    # Pads
    "Pad1 (new age)",
    "Pad2 (warm)",
    "Pad3 (polysynth)",
    "Pad4 (choir)",
    "Pad5 (bowed)",
    "Pad6 (metallic)",
    "Pad7 (halo)",
    "Pad8 (sweep)",
]

fx = [
    # FX
    "FX1 (rain)",
    "FX2 (soundtrack)",
    "FX 3 (crystal)",
    "FX 4 (atmosphere)",
    "FX 5 (brightness)",
    "FX 6 (goblins)",
    "FX 7 (echoes)",
    "FX 8 (sci-fi)",
]

international = [
    # International
    "Sitar",
    "Banjo",
    "Shamisen",
    "Koto",
    "Kalimba",
    "Bag pipe",
    "Fiddle",
    "Shanai",
    "Tinkle Bell",
]


# Drums
drums = [
    "Agogo",
    "Steel Drums",
    "Woodblock",
    "Taiko Drum",
    "Melodic Tom",
    "Synth Drum",
]


goofs = [
    # Goofs
    "Reverse Cymbal",
    "Guitar Fret Noise",
    "Breath Noise",
    "Seashore",
    "Bird Tweet",
    "Telephone Ring",
    "Helicopter",
    "Applause",
    "Gunshot",
]

polyphonic = [
    keyboards,
    guitars,
    strings,
    voices,
    orchestra,
    pads,
    goofs,
]
monophonic = [
    fx,
    wind_instruments,
    basses,
    leads,
    international,
    drums,
]


def track_creator(instrument_name, channel):
    instrument = MidiInstrument()
    track = Track(instrument, channel=channel)
    instrument.name = instrument_name
    track.instrument.instrument_nr = MidiInstrument.names.index(instrument_name)
    return track


def midi_file_name(instrument_name):
    nice_inst = re.sub(r"[\s+()]", "", instrument_name).lower()
    return Path(__file__).parent.parent.joinpath(f"midi_files/{nice_inst}.mid")


def generate_applause():
    applause_track = track_creator("Applause", channel=4)
    bar = Bar("C", (4, 4))
    nc = NoteContainer("C", octave=2)
    bar.place_notes(nc, 1)
    applause_track.add_bar(bar)
    return applause_track


def add_4_4(track, note, octave=2, rhythm=[4, 4, 4, 4]):
    bar = Bar(note, (4, 4))
    nc = NoteContainer(note, octave=octave)
    for length in rhythm:
        bar.place_notes(nc, length)
        track.add_bar(bar)
    return track


def choose_rhythm():
    total_weight = sum([rhythm["weight"] for rhythm in CHORD_RHYTHMS])
    rhythm_choice = randint(0, total_weight - 1)

    choice_list = []
    for index, rhythm_info in enumerate(CHORD_RHYTHMS):
        for _ in range(rhythm_info["weight"]):
            choice_list.append(rhythm_info["rhythm"])

    choosen_rhythm = choice_list[rhythm_choice]
    random.shuffle(choosen_rhythm)
    return choosen_rhythm


def find_polyphony_limit(instrument, chord):
    polyphony_limit = INSTRUMENT_POLYPHONY.get(instrument, None)

    if polyphony_limit is None:
        # Create a list full of the values from other lists

        if instrument in [item for sublist in polyphonic for item in sublist]:
            return len(chord)
        else:
            return 1

    return polyphony_limit


# Depends on the instrument
def choose_notes(key, chord, instrument, previous_notes=None):
    polyphony_limit = find_polyphony_limit(instrument, chord)
    # We must go further

    scale = Major(key).ascending()
    # breakpoint()
    # print(f"Scale: {scale}")
    # print(f"Key: {key}")
    if randint(0, 1):
        return random.sample(chord, random.randint(1, polyphony_limit))
    else:
        if randint(0, 1) or previous_notes is None:
            return random.sample(scale, 1)[0]
        else:
            previous_note = (
                previous_notes[0]
                if (isinstance(previous_notes, list))
                else previous_notes
            )

            note_pos = scale.index(previous_note)
            lower_note_pos = note_pos - 1
            upper_note_pos = (note_pos + 1) if note_pos != len(scale) else 0
            return scale[random.sample([lower_note_pos, upper_note_pos], 1)[0]]
            # return scale[random.sample([ note_pos - 1, note_pos + 1 ], 1)[0]]


# A#, D#, G#
def generate_midi(
    *, instrument, chord_progression, pad, key, bpm=120, octave=None, applause=False
):
    composition = Composition()

    how_many_bars = 16

    chord_track = Track(instrument, channel=1)

    # make a method that only returns random instrument
    # that deemed lead worthy
    melody_instrument = random.sample(monophonic, 1)[0]
    melody_track = Track(melody_instrument, channel=2)

    drone_track = track_creator(pad, channel=6)

    # It's one of the few pitched drums
    timpani_track = track_creator("Timpani", channel=3)

    if not octave:
        octave = int(INSTRUMENT_OCTAVE.get(instrument.name, 4))

    for _ in range(how_many_bars):
        for beat, chord in enumerate(chord_progression, start=1):
            bar = Bar(key, (4, 4))

            some_notes = None
            for length in choose_rhythm():
                some_notes = choose_notes(
                    key, chord, instrument.name, previous_notes=some_notes
                )
                # print(some_notes)
                nc = NoteContainer(some_notes, octave=octave)
                bar.place_notes(nc, length)
            chord_track.add_bar(bar)

            add_4_4(drone_track, chord[0], rhythm=[1])
            add_4_4(timpani_track, chord[0])

    composition.add_track(timpani_track)
    composition.add_track(drone_track)
    composition.add_track(chord_track)

    # Do we want to add the channel when adding or creating the track?
    if applause:
        applause_track = generate_applause()
        composition.add_track(applause_track)

    instrument_name = MidiInstrument.names[instrument.instrument_nr]
    write_Composition(midi_file_name(instrument_name), composition, bpm=bpm)
