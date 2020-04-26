# Sandberg

Project for generating songs for you to play along with, built on Twitch using
python and the mingus library.

## Overview

mingus to generate the Midi
fluidsynth to play the midi

## Goals

Generate songs, passing in various options to change things like:

- Style
- Instruments
- Harmonic Complexity
- BPM
- Rhythm Choices
- Drums

Overlay images for the music video with FFMPEG

## Meta-Goals

Learn Music Theory From this
Drain our Ears From this

- Recognizing progressions
- Recognize interval over a chord

## Install Requirements

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/runtime.in
```

## Usage

Generating Midi

```bash
python music.py
```

Generating Individual Album Art

```bash
python art.py
```

Generate Music Video

```bash
./hit_machine Trees
```
