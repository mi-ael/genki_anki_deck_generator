python projekt for extracting vocabulary sounds from official genki audio files and generating anki decks
Genki 1: https://ankiweb.net/shared/info/1742947823
Genki 2 (WIP): https://ankiweb.net/shared/info/969261095

# How to build
- clone repo
- install ffmpeg
- run: python -m venv venv
- run: source venv/bin/activate
- run: pip install -r requirements.txt
- run: python download_genki_sound_files.py
- run: python main.py
- ...
- profit

# Project Structure
- Folders in data/ directory are turned into anki-decks
- deck generation uses yaml files in templates/ directory

# Template file explanation
- "sound_file": (string) sound file used for this deck (starts searching in sound/ directory)
- "skip_on_beginning": (integer) how many words should be skiped at the beginning of the sound file
- "skip_with_new_category": (boolean) if true skips a word if new category starts
- "skip_on_semikolon": (boolean) if true skips as many words as there are semikolons in the english translation, after a note
- "uid": (integer) uniqe id, used for anki (should not be too high)
- "sound_silence_threshold": (integer) magic number used for splitting genki-audiofiles into many seperate words. (default: 600)
- "cards": list of categories
- "category": (string) name of the category (only matters for tags)
- "vocabulary": list of vocabs
- "japanese": (string) japanese meaning in kana
- "english": (string) english meaning
- "kanji": (string) japanese meaning in kanji (should be left out, if the vocab has no kanjis)

# Notes
- I have only tested this under linux

# Pull-Requests Welcome
- add Windows support (if you care)
- extend Deck for Genki II
- write a better description for the anki deck
- add devops
- bugfixes, etc.

# copyright note
I do not own the Copyright to the Genki audiofiles (thats why they are not inculded in this repo and downloaded elsewhere) but they are puplicly available without needing to prove ownership of a genki book.
