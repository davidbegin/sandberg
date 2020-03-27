import random

from mingus.containers.instrument import MidiInstrument


class Waitstaff:
    names = MidiInstrument.names
    keyboards = names[0:24]
    guitars   = names[24:32]
    instrument_groups = {
        "Keyboard" : (0, 24),
        "Guitar": (24, 32),
    }
    
    @staticmethod
    def choose_from_group(group):
        start, end = Waitstaff.instrument_groups[group]
        return random.sample(Waitstaff.names[start:end], 1)[0]

    @staticmethod
    def show_choices():
        # basses = names[24:32]
        # strings = names[24:54]

        # names = [
        #     "Acoustic Grand Piano",
        #     "Bright Acoustic Piano",
        #     "Electric Grand Piano",
        #     "Honky-tonk Piano",
        #     "Electric Piano 1",
        #     "Electric Piano 2",
        #     "Harpsichord",
        #     "Clavi",
        #     "Celesta",
        #     "Glockenspiel",
        #     "Music Box",
        #     "Vibraphone",
        #     "Marimba",
        #     "Xylophone",
        #     "Tubular Bells",
        #     "Dulcimer",
        #     "Drawbar Organ",
        #     "Percussive Organ",
        #     "Rock Organ",
        #     "Church Organ",
        #     "Reed Organ",
        #     "Accordion",
        #     "Harmonica",
        #     "Tango Accordion",

        #     # Guitars
        #     "Acoustic Guitar (nylon)",
        #     "Acoustic Guitar (steel)",
        #     "Electric Guitar (jazz)",
        #     "Electric Guitar (clean)",
        #     "Electric Guitar (muted)",
        #     "Overdriven Guitar",
        #     "Distortion Guitar",
        #     "Guitar harmonics",

        #     # Basses
        #     "Acoustic Bass",
        #     "Electric Bass (finger)",
        #     "Electric Bass (pick)",
        #     "Fretless Bass",
        #     "Slap Bass 1",
        #     "Slap Bass 2",
        #     "Synth Bass 1",
        #     "Synth Bass 2",

        #     # Strings
        #     "Violin",
        #     "Viola",
        #     "Cello",
        #     "Contrabass",
        #     "Tremolo Strings",
        #     "Pizzicato Strings",
        #     "Orchestral Harp",
        #     "Timpani",
        #     "String Ensemble 1",
        #     "String Ensemble 2",
        #     "SynthStrings 1",
        #     "SynthStrings 2",

        #     # Voices
        #     "Choir Aahs",
        #     "Voice Oohs",
        #     "Synth Voice",

        #     # Orchestra
        #     "Orchestra Hit",
        #     "Trumpet",
        #     "Trombone",
        #     "Tuba",
        #     "Muted Trumpet",
        #     "French Horn",
        #     "Brass Section",
        #     "SynthBrass 1",
        #     "SynthBrass 2",
        #     "Soprano Sax",
        #     "Alto Sax",
        #     "Tenor Sax",
        #     "Baritone Sax",
        #     "Oboe",
        #     "English Horn",
        #     "Bassoon",
        #     "Clarinet",
        #     "Piccolo",
        #     "Flute",

        
        #     # Wind Things
        #     "Recorder",
        #     "Pan Flute",
        #     "Blown Bottle",
        #     "Shakuhachi",
        #     "Whistle",
        #     "Ocarina",


        #     # Leads
        #     "Lead1 (square)",
        #     "Lead2 (sawtooth)",
        #     "Lead3 (calliope)",
        #     "Lead4 (chiff)",
        #     "Lead5 (charang)",
        #     "Lead6 (voice)",
        #     "Lead7 (fifths)",
        #     "Lead8 (bass + lead)",


        #     # Pads
        #     "Pad1 (new age)",
        #     "Pad2 (warm)",
        #     "Pad3 (polysynth)",
        #     "Pad4 (choir)",
        #     "Pad5 (bowed)",
        #     "Pad6 (metallic)",
        #     "Pad7 (halo)",
        #     "Pad8 (sweep)",

        #     # FX
        #     "FX1 (rain)",
        #     "FX2 (soundtrack)",
        #     "FX 3 (crystal)",
        #     "FX 4 (atmosphere)",
        #     "FX 5 (brightness)",
        #     "FX 6 (goblins)",
        #     "FX 7 (echoes)",
        #     "FX 8 (sci-fi)",


        #     # International
        #     "Sitar",
        #     "Banjo",
        #     "Shamisen",
        #     "Koto",
        #     "Kalimba",
        #     "Bag pipe",
        #     "Fiddle",
        #     "Shanai",
        #     "Tinkle Bell",


        #     # Drums
        #     "Agogo",
        #     "Steel Drums",
        #     "Woodblock",
        #     "Taiko Drum",
        #     "Melodic Tom",
        #     "Synth Drum",


        #     # Goofs
        #     "Reverse Cymbal",
        #     "Guitar Fret Noise",
        #     "Breath Noise",
        #     "Seashore",
        #     "Bird Tweet",
        #     "Telephone Ring",
        #     "Helicopter",
        #     "Applause",
        #     "Gunshot",
        # ]

        for index, name in enumerate(Waitstaff.names):
            print(f"{index} - {name}")
