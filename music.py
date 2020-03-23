import random
import os



import roman
import mingus.core.progressions as progressions
import mingus.core.chords as chords
import mingus.core.notes as notes
import mingus.core.scales as scales
from mingus.containers.note_container import NoteContainer
from mingus.containers import Bar
from mingus.containers import Track
from mingus.containers.instrument import MidiInstrument


from mingus.midi.midi_file_out import MidiFile as MidiFileOut
from mingus.midi.midi_file_out import write_NoteContainer
from mingus.midi.midi_file_out import write_Bar
from mingus.midi.midi_file_out import write_Track



def convert_roots_to_chord_chart(roots, scale_notes):
    return [
        roman.toRoman(scale_notes.index(root) + 1) for root in roots
    ]

# Fux / Bach Rules 
CLASSICAL_HARMONY = {
        1: [2, 3, 4, 5, 6, 7],
        2: [5, 7, 1],
        3: [6, 4],
        4: [2, 5, 7, 1],
        5: [1, 6],
        6: [4, 2],
        7: [1, 6]
}


def roman_chord_fmt(chord_position):
    rome = f"{roman.toRoman(chord_position)}"
    if chord_position not in [1,4,5]:
        return rome.lower()
    return rome


def chord_fmt(chord, chord_position):
    if chord_position == 7:
        return f"{chord}dim"
    elif chord_position not in [1,4,5]:
        return f"{chord}m"
    return chord



def progress(chord_position):
    next_chord_int = random.choice(CLASSICAL_HARMONY[chord_position])
    next_chord = scale_notes[next_chord_int - 1]
    print(f"{roman_chord_fmt(next_chord_int)}: {chord_fmt(next_chord, next_chord_int)}")
    return next_chord, next_chord_int

if __name__ ==  "__main__":
    os.system("clear")
    song = [ ]

    key_int     = random.randint(0,11)
    key         = notes.int_to_note(key_int)
    scale       = scales.Diatonic(key, (3,7))
    scale_notes = scale.ascending()
    song.append(key)
    print(f"I: {key}")

    # Getting the 2nd
    next_chord, next_chord_int = progress(1)
    song.append(next_chord)

    while True:
        next_chord, next_chord_int = progress(next_chord_int)
        song.append(next_chord)
        if len(song) % 2 == 0 and next_chord_int in [1,6]:
            break

    instrument = MidiInstrument()

    # Ocarina
    instrument.instrument_nr = 79

    instrument.instrument_nr = random.randint(0, len(MidiInstrument.names))

    track = Track(instrument)
    chord_chart = convert_roots_to_chord_chart(song, scale_notes[:-1])
    chord_progression = progressions.to_chords(chord_chart, key) 

    # Can't handle Sharp keys for some reason
    for _ in range(16):
        for chord in chord_progression:
            bar = Bar(key, (4, 4))
            nc = NoteContainer(chord)
            bar.place_notes(nc, 4)
            bar.place_notes(nc, 3)
            bar.place_notes(nc, 4)
            bar.place_notes(nc, 5)
            bar.place_notes(nc, 8)
            track.add_bar(bar)

    write_Track("midi_files/test.mid", track, bpm=120)
