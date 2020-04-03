from random import randint, shuffle, sample

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


def split_bar(bar):
    return [item for sublist in [split_note(note) for note in bar] for item in sublist]


def split_note(note):
    return [note * 2] * 2


def generate_rhythm():
    rhythms = [rhythm["rhythm"] for rhythm in CHORD_RHYTHMS]
    return sample(rhythms, 1)[0]


def choose_rhythm(time_signature):
    total_weight = sum([rhythm["weight"] for rhythm in CHORD_RHYTHMS])
    rhythm_choice = randint(0, total_weight - 1)

    choice_list = []
    for index, rhythm_info in enumerate(CHORD_RHYTHMS):
        for _ in range(rhythm_info["weight"]):
            choice_list.append(rhythm_info["rhythm"])

    choosen_rhythm = choice_list[rhythm_choice]
    shuffle(choosen_rhythm)
    return choosen_rhythm
