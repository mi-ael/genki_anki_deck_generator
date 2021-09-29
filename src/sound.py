from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from typing import List
from pathlib import Path
from cachier import cachier
from src.data import Card, Deck

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


@cachier(cache_dir=os.getenv('CACHE_DIR', '/tmp/genki_anki_generator_cache'))
def extract_words_from_soundfile(file: str, sound_silence_threshold: int):
    sound_file = AudioSegment.from_mp3(file)
    audio_chunks = split_on_silence(sound_file, 
        keep_silence=True,
        min_silence_len=sound_silence_threshold,
        silence_thresh=-32
        )
    for i,sound in enumerate(audio_chunks):
        start_trim = detect_leading_silence(sound)
        audio_chunks[i] = sound[start_trim:]
    return audio_chunks

def extract_japanese_words_from_soundfile_and_save(dst_dir: Path, deck: Deck, save_all: bool = False):
    words = extract_words_from_soundfile(deck.sound_file, deck.sound_silence_threshold)

    cards: List[Card] = deck.cards
    word_paths = [None] * len(cards)
    next_word_jap = True
    vocab_index = 0 # seperate for eng and jap
    sound_index = 0 # index for extracted sounds

    def export_sound_file(sound: AudioSegment, card: Card, suffix: str) -> str:
        parts = []
        parts.append(deck.name.replace(" ", "_"))
        parts.append(str(sound_index).zfill(3))
        if card is not None:
            parts.append(card.get_beautyfied_english_name())
        parts.append(suffix)
        filename = dst_dir.joinpath(f"{'_'.join(parts)}.mp3")
        print(f"exporting: {filename}")
        sound.export(filename, format="mp3")
        return filename


    while sound_index < len(words):
        skip_file = sound_index in deck.skip_words or vocab_index >= len(cards)*2
        sound = words[sound_index]
        card_index = vocab_index // 2
        if deck.only_japanese:
            card_index = vocab_index
        card = cards[card_index] if not skip_file else None # todo fix
        if card is not None and card.custom_threshold_eng is not None and next_word_jap == False:
            name = export_sound_file(sound, None, "split")
            new_words = extract_words_from_soundfile(name, card.custom_threshold_eng)
            del words[sound_index]
            for w in reversed(new_words):
                words.insert(sound_index, w)
            sound = words[sound_index]
        if card is not None and card.custom_threshold_jap is not None and next_word_jap == True:
            name = export_sound_file(sound, None, "split")
            new_words = extract_words_from_soundfile(name, card.custom_threshold_jap)
            del words[sound_index]
            for w in reversed(new_words):
                words.insert(sound_index, w)
            sound = words[sound_index]

        if skip_file == True: # skip
            if save_all:
                export_sound_file(sound, None, "skiped")
        elif next_word_jap == True: # jap
            if card.fuse_with_next:
                for i in range(card.fuse_with_next):
                    sound = sound.append(words[sound_index+i+1], crossfade=0)
                sound_index += card.fuse_with_next
            filename = export_sound_file(sound, card, "jap")
            word_paths[card_index] = filename
        else: # eng
            if save_all:
                export_sound_file(sound, card, "eng")

        if not skip_file:
            next_word_jap = not next_word_jap or deck.only_japanese
            vocab_index += 1
        sound_index += 1

    assert(all(word_paths)) # every Card must have a sound

    return word_paths

        
