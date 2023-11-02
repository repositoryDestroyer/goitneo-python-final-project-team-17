import json

from json.decoder import JSONDecodeError


def load_notes(notes_json):
    try:
        with open(notes_json, 'r') as f:
            notes = json.load(f)
    except (FileNotFoundError, AttributeError, JSONDecodeError):
        notes = {}
    return notes


def dump_notes(notes_json, notes):
    with open(notes_json, 'w') as f:
        if notes:
            json.dump(notes, f)