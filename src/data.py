from typing import List
import sys
import ruamel.yaml
from src.kanji_fetcher import fetch_kanjis, fetch_kanji_meanings
from pathlib import Path


class Card:
    def __init__(self, japanese: str, english: str, kanjis: str):
        self.japanese: str = japanese
        self.english: str = english
        self.sound_file: str = None
        self.kanjis:str = kanjis
        self.kanjis_meanings: List[str] = []
        self.category: str = ""
        self.tags: List[str] = []
        self.fuse_with_next: int = 0
    
    def get_beautyfied_english_name(self):
        name = self.english.\
            replace(" ", "_").\
            replace("/", "").\
            replace(".", "").\
            replace(";", "").\
            replace("__", "_").\
            replace("__", "_").\
            replace("'", "")
        return ''.join(e for e in name if e.isalnum() or e == '_')

    def validate(self):
        return True

class Deck:
    def __init__(self):
        self.name: str = ""
        self.sound_file: Path = None
        self.skip_words: List[int] = []
        self.cards: List[Card] = []
        self.uid: int = None
        self.skip_with_new_category: bool = False
        self.skip_on_beginning: int = 0
        self.skip_on_semikolon: bool = True
        self.sound_silence_threshold: int = None
        self.only_japanese: bool = False

    def validate(self):
        return True # todo


    def load_sound_files(self, resources: Path, media_output_path: Path):
        from src.sound import extract_japanese_words_from_soundfile_and_save

        if self.sound_file == None: return

        #names = [c.english.replace(" ", "_").replace("/", "").replace(".", "").replace(";", "").replace("__", "_").replace("__", "_").replace("'", "") for c in self.cards]
        #names = [self.name.replace(" ", "_") + '_' + ''.join(e for e in c if e.isalnum() or c == '_') for c in names]
        #sound_files = extract_japanese_words_from_soundfile_and_save(self.sound_file, media_output_path, names, skip=self.skip_words, save_all=True, sound_silence_threshold=self.sound_silence_threshold, only_japanese=self.only_japanese, fuse_list=[c.fuse_with_next for c in self.cards])
        sound_files = extract_japanese_words_from_soundfile_and_save(media_output_path, self, save_all=True)

        for c, sf in zip(self.cards, sound_files):
            c.sound_file = sf

    def load_kanji_data(self):
        for c in self.cards:
            if c.fetch_kanjis is True:
                c.kanjis = fetch_kanjis(c.japanese[0])

    def load_kanji_meaning_data(self):
        for c in self.cards:
            if c.kanjis != "":
                c.kanjis_meanings = [fetch_kanji_meanings(k) for k in filter(lambda x: x != '.', c.kanjis)]

    @staticmethod
    def parse_vocab(subtag, deck, cat, c, skip_index) -> int:
        for e in c["vocabulary"]:
            skip_index = skip_index+2
            card = Card(e["japanese"], e["english"], e.get("kanji", ""))
            card.category = cat
            card.tags.append(cat)
            card.fuse_with_next = e.get("fuse_with_next", 0)
            if subtag is not None:
                card.tags.append(subtag)
            deck.cards.append(card)
            if "skip_on_semikolon" not in e and deck.skip_on_semikolon or "skip_on_semikolon" in e and (e["skip_on_semikolon"] == True or (type(e["skip_on_semikolon"]) == int and e["skip_on_semikolon"] != 0)):
                skips = card.english.replace("&nbsp;", "").count(';')
                if "skip_on_semikolon" in e and type(e["skip_on_semikolon"]) == int:
                    skips = e["skip_on_semikolon"]
                for _ in range(skips):
                    deck.skip_words.append(skip_index)
                    skip_index = skip_index+1
        return skip_index

    @staticmethod
    def parse(file: Path, resources: Path):
        deck = Deck()
        yaml = ruamel.yaml.YAML()
        doc = yaml.load(open(file))
        if doc.get("sound_file", "") == "" or doc.get("sound_file", None) is None:
            deck.sound_file = None
        else:
            deck.sound_file = resources.joinpath(doc["sound_file"])
        deck.skip_words = doc.get("skip_words", [])
        deck.uid = doc["uid"]
        deck.skip_on_beginning = doc.get("skip_on_beginning", 2)
        deck.skip_words.extend(range(deck.skip_on_beginning))
        skip_index = deck.skip_on_beginning
        deck.skip_with_new_category = doc.get("skip_with_new_category", True)
        deck.skip_on_semikolon = doc.get("skip_on_semikolon", True)
        deck.sound_silence_threshold = doc.get("sound_silence_threshold", 600)
        deck.only_japanese = doc.get("only_japanese", False)
        for c in doc["cards"]:
            if deck.skip_with_new_category:
                deck.skip_words.append(skip_index)
                skip_index = skip_index+1
            cat = c.get("category", "")
            
            if "category" in c["vocabulary"][0]:
                for s in c["vocabulary"]:
                    if deck.skip_with_new_category:
                        deck.skip_words.append(skip_index)
                        skip_index = skip_index+1
                    scat = s.get("category", "")
                    skip_index = Deck.parse_vocab(scat, deck, cat, s, skip_index)
            else:
                skip_index = Deck.parse_vocab(None, deck, cat, c, skip_index)
            
        return deck

class MetaDeck:
    def __init__(self):
        self.name: str = ""
        self.decks = []