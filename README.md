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

## Install Requirements

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/runtime.in
```

