from src.data import Deck, Card, MetaDeck
import genanki
from typing import List

html_kanji_kana = """
<font lang="jp" size="6px" color="#C0C0C0"><span class="japanese">{{kanjis}}</span></font>
<br>
<font lang="jp" size="15px"><span class="japanese">{{japanese_kana}}</span></font>
<br>
"""

html_sound="""
{{sound}}
<br>
"""

html_frontside="""
{{FrontSide}}
"""

html_meaning="""
<font lang="jp" size="4px" color="#C0C0C0">Meaning: </font>
<br>
"""

html_english="""
<font lang="jp" size="15px"><span class="text">{{english}}</span></font>
<br>
"""

html_kanji_meaning="""
<br>
{{#kanji_meaning}}
<font lang="jp" size="4px" color="#C0C0C0">Kanji Meaning: </font>
<br>
<font lang="jp" size="6px"><span class="japanese">{{kanjis}}</span></font>
<br>
<font lang="jp" size="6px"><span class="text">{{kanji_meaning}}</span></font>
<br>
{{/kanji_meaning}}
"""

css="""

.card {
  font-family: "Noto Sans Japanese";
  font-size: 20px;
  text-align: center;
}

@font-face {
  font-family: "Noto Sans Japanese";
  src: url("_NotoSansCJKjp-Regular.woff2") format("woff2");
}

.japanese {
 font-family: "Noto Sans Japanese";
}

"""


class GenkiNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[7]) # uid

    @property
    def sort_field(self):
        return self.fields[7] # sort_id

    
    @sort_field.setter
    def sort_field(self, value):
        pass
            

def gen_deck(deck: Deck, deckpath: str, model: genanki.Model) -> genanki.Deck:
    full_name = f'{deckpath}::{deck.name}'
    anki_deck = genanki.Deck(deck.uid, full_name)
    i = 0
    for c in deck.cards:
        note = GenkiNote(
            model=model,
            fields=[
                c.japanese, 
                c.kanjis, 
                "", 
                c.english, 
                c.kanjis_meanings,
                f"[sound:{c.sound_file.name}]" if c.sound_file is not None else "",
                str(i),
                f'{full_name}_{i}'
            ],
            tags=c.tags
            )
        i+=1
        anki_deck.add_note(note)
    return anki_deck
    
def walk_deck(decklike, deckpath: str, model: genanki.Model, anki_decks:[], sound_files:[]):
    if isinstance(decklike, MetaDeck):
        metadeck: MetaDeck = decklike
        new_deckpath = f"{deckpath}::{metadeck.name}" if deckpath != '' else metadeck.name
        for deck in metadeck.decks:
            walk_deck(deck, new_deckpath, model, anki_decks, sound_files)
    else:
        deck:Deck = decklike
        anki_deck = gen_deck(deck, deckpath, model)
        sound_files.extend([c.sound_file for c in deck.cards if c.sound_file is not None])
        anki_decks.append(anki_deck)


def export_to_anki(decks: List):
    
    
    anki_model = genanki.Model(
        1561628563,
        'Simple Model',
        fields=[
            {'name': 'japanese_kana'},
            {'name': 'kanjis'},
            {'name': 'type'},
            {'name': 'english'},
            {'name': 'kanji_meaning'},
            {'name': 'sound'},
            {'name': 'sort_id'},
            {'name': 'uid'},
        ],
        templates=[
            {
            'name': 'japanese -> english',
            'qfmt': html_kanji_kana + html_sound,
            'afmt': html_frontside + html_meaning + html_english + html_kanji_meaning,
            },
            {
            'name': 'english -> japanese',
            'qfmt': html_english,
            'afmt': html_frontside + html_meaning + html_kanji_kana + html_kanji_meaning + html_sound,
            },
        ],
        css=css
        )
    anki_decks = []
    sound_files = []
    for d in decks:
        walk_deck(d, "", anki_model, anki_decks, sound_files)
    
    anki_package = genanki.Package(anki_decks)

    # font
    sound_files.append("data/fonts/_NotoSansCJKjp-Regular.woff2")

    anki_package.media_files = sound_files

    anki_package.write_to_file('genki.apkg')
