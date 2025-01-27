import json
import urllib.request
import pprint
import gen_additional_kanji_data
pp = pprint.PrettyPrinter(indent=2)
from ruamel.yaml import YAML
yaml=YAML()
import os
from typing import List
from num2words import num2words

# todo: additional vocab eg. 11

def num2kanji(num):
    if num == '0':
        return None
    return num2words(num, lang='ja')

def apply_hacks(cat, i, tag, stag=None):
    if i == 0 and tag == 'School':
        for v in cat['vocabulary']:
            if v['japanese'] == 'いちねんせい':
                v['kanji'] = '一年生'
    if i == 0 and tag == 'Others':
        cat['vocabulary'].insert(6, {'japanese': '〜ばん', 'english': 'number ...', 'kanji': ''})
    if i == 0 and tag == 'Expressions':
        del cat['vocabulary'][len(cat['vocabulary'])-1]
        cat['vocabulary'].append({'japanese': 'そうですか。', 'english': 'I see.', 'kanji': ''})
        cat['vocabulary'].append({'japanese': 'そうですか？', 'english': 'Is that so?', 'kanji': ''})
    if i == 1 and tag == 'Majors':
        eng = cat['vocabulary'].pop(len(cat['vocabulary'])-1)
        cat['vocabulary'].insert(0, eng)
    if i == 2 and tag == 'U-verbs':
        for v in cat['vocabulary']:
            if v['japanese'] == 'きく':
                v['skip_on_semicolon'] = 1
    if i == 3 and stag == 'People_and_Things':
        desk = cat['vocabulary'].pop(0)
        chair = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(5, chair)
        cat['vocabulary'].insert(6, desk)
    if i == 4 and tag == 'い-adjectives':
        for v in cat['vocabulary']:
            if v['japanese'] == 'さむい':
                v['skip_on_semicolon'] = 2
    if i == 4 and tag == 'U-verbs':
        ask = cat['vocabulary'].pop(0)
        ask['skip_on_semicolon'] = 0
        cat['vocabulary'].insert(1, ask)
    if i == 5 and tag == 'Nouns':
        electricity = cat['vocabulary'].pop(0)
        window = cat['vocabulary'].pop(0)
        this = cat['vocabulary'].pop(0)
        next_w = cat['vocabulary'].pop(0)
        next_y = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(9, electricity)
        cat['vocabulary'].insert(10, window)
        cat['vocabulary'].insert(13, this)
        cat['vocabulary'].insert(14, next_w)
        cat['vocabulary'].insert(15, next_y)
    if i == 5 and tag == 'U-verbs':
        for v in cat['vocabulary']:
            if v['japanese'] == 'やすむ':
                v['skip_on_semicolon'] = 1
    if i == 6 and tag == 'Nouns':
        os = cat['vocabulary'].pop(0)
        ob = cat['vocabulary'].pop(0)
        ys = cat['vocabulary'].pop(0)
        yb = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(3, ob)
        cat['vocabulary'].insert(4, os)
        cat['vocabulary'].insert(9, ys)
        cat['vocabulary'].insert(10, yb)
    if i == 7 and tag == 'Nouns':
        ow = cat['vocabulary'].pop(0)
        td = cat['vocabulary'].pop(0)
        tm = cat['vocabulary'].pop(0)
        nm = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(10, td)
        cat['vocabulary'].insert(12, tm)
        cat['vocabulary'].insert(13, nm)
        cat['vocabulary'].insert(14, ow)
    if i == 7 and tag == 'Adverbs_and_Other_Expressions':
        for v in cat['vocabulary']:
            if v['english'] == 'not ... yet':
                v['skip_on_semicolon'] = 1
    if i == 8 and tag == 'Nouns':
        lm = cat['vocabulary'].pop(0)
        ly = cat['vocabulary'].pop(0)
        cat['vocabulary'].append(lm)
        cat['vocabulary'].append(ly)
    if i == 8 and tag == 'Ru-verbs':
        for v in cat['vocabulary']:
            if v['japanese'] == 'でる':
                v['skip_on_semicolon'] = 2
    if i == 9 and tag == 'Nouns':
        d = cat['vocabulary'].pop(0)
        ty = cat['vocabulary'].pop(0)
        f = cat['vocabulary'].pop(0)
        a = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(7, a)
        cat['vocabulary'].insert(11, d)
        cat['vocabulary'].insert(14, f)
        cat['vocabulary'].append(ty)
    if i == 9 and tag == 'U-verbs':
        for v in cat['vocabulary']:
            if v['japanese'] == 'かかる':
                v['skip_on_semicolon'] = 1
    if i == 9 and tag == 'Adverbs_and_Other_Expressions':
        for v in cat['vocabulary']:
            if v['japanese'] == 'どっち／どちら':
                v['skip_on_semicolon'] = 1
            if v['japanese'] == '〜しゅうかん':
                v['skip_on_semicolon'] = 1
            if v['japanese'] == '〜かげつ':
                v['skip_on_semicolon'] = 1
    if i == 10 and tag == 'Nouns':
        aus = cat['vocabulary'].pop(0)
        cat['vocabulary'].insert(1, aus)
    if i == 11 and tag == 'Nouns':
        pol = cat['vocabulary'].pop(0)
        too = cat['vocabulary'].pop(0)
        men = cat['vocabulary'].pop(2)
        cat['vocabulary'].insert(3, too)
        cat['vocabulary'].insert(20, pol)
        cat['vocabulary'].append(men)
    if i == 11 and tag == 'い-adjectives':
        for v in cat['vocabulary']:
            if v['japanese'] == 'せまい':
                v['skip_on_semicolon'] = False
    if i == 11 and tag == 'Adverbs_and_Other_Expressions':
        for v in cat['vocabulary']:
            if v['japanese'] == 'もうすぐ':
                v['skip_on_semicolon'] = 2

    for v in cat['vocabulary']:
        if 'kanji' in v:
            v['kanji'] = v['kanji'].replace('... ', '〜').replace('...', '〜')

                
        




                


                

        


    

def remove_from_list(l, elem) -> List:
    #if elem in l:
    l = l.copy()
    l.remove(elem)
    return l

def get_subtags(vocab, tag):
    tags = [tuple(remove_from_list(list(filter(lambda x: not x.endswith('Vocabulary'), x['tags'])), tag)) for x in vocab]
    tags = unique(tags)
    tags = list(filter(lambda x: len(x) == 1, tags))
    return tags


def unique(l):
    # requires python 3.7 for order
    return list(dict.fromkeys(l))


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def get_out_dict(mayor, sound_file=None, minor=0):
    return {
        'sound_file': sound_file,
        'skip_words': [],
        'skip_on_beginning': 2,
        'skip_with_new_category': True,
        'skip_on_semicolon': True,
        'uid': 693904000 + mayor*100 + minor,
        'sound_silence_threshold': 600,
        'cards': [],
    }

kanji_data = gen_additional_kanji_data.get_kanji_data()

result = invoke('deckNamesAndIds')
#print(result)
result = list(filter(lambda v: v[0].startswith('Genki_I::'), result.items()))
vocab = []
vocab_sound_files = [
    'Kaiwa_Bunpo_L01/K01_05.mp3',
    'Kaiwa_Bunpo_L02/K02_05.mp3',
    'Kaiwa_Bunpo_L03/K03_05.mp3',
    'Kaiwa_Bunpo_L04/K04_07.mp3',
    'Kaiwa_Bunpo_L05/K05_07.mp3',
    'Kaiwa_Bunpo_L06/K06_07.mp3',
    'Kaiwa_Bunpo_L07/K07_05.mp3',
    'Kaiwa_Bunpo_L08/K08_05.mp3',
    'Kaiwa_Bunpo_L09/K09_07.mp3',
    'Kaiwa_Bunpo_L10/K10_05.mp3',
    'Kaiwa_Bunpo_L11/K11_07.mp3',
    'Kaiwa_Bunpo_L12/K12_05.mp3',
]
for i in range(1, 13):
    cards = invoke('findNotes', query=f'"deck:Genki_I::L{i}"')
    card = invoke('notesInfo', notes=cards)
    current_vocab = []
    for e in card:
        note = {}
        fields = e['fields']
        note['jap'] = fields['Vorderseite']['value']
        note['kan'] = fields['Kanji']['value']
        if i == 1 or i == 2 and note['kan'] == '':
            dic = kanji_data[i-1]
            jap = note['jap'].replace("〜", "")
            if jap in dic:
                note['kan'] = kanji_data[i-1][jap]
        note['eng'] = fields['Rückseite']['value']
        note['tags'] = e['tags']
        current_vocab.append(note)
    vocab.append(current_vocab)
all_past_cards = []
structured_vocab = []
for i,deck in enumerate(vocab):
    all_past_cards.extend(deck)
    if i == 0:
        tag_vocab = list(filter(lambda x: any([y.endswith('Vocabulary') for y in x['tags']]) 
            and all([not y.endswith('Additional_Vocabulary') for y in x['tags']]) 
            and 'Useful_Expressions' not in x['tags']
            or x['jap'] == 'いちじ'
            , deck))
    #elif i == 1:
    #    tag_vocab = list(filter(lambda x: any([y.endswith('Vocabulary') for y in x['tags']]) 
    #        #and 'Useful_Expressions' not in x['tags']
    #        , deck))
    else:
        tag_vocab = list(filter(lambda x: any([f'L{i+1}_Vocabulary' == y for y in x['tags']]) 
            , all_past_cards))
    if i == 1:
        tags = [('Words_That_Point',), ('Food',), ('Things',), ('Places',), ('Countries',), ('Majors',), ('Family',), ('Money_Matters',), ('Expressions',)]
    else:
        tags = [tuple(filter(lambda e: not e.endswith('Vocabulary'), x['tags'])) for x in tag_vocab]
        if i in [2,3,4,5,6,7,8,9]:
            tags = [("Nouns",)] + tags
        tags = unique(tags)
        tags = list(filter(lambda x: len(x) == 1, tags))
        if i==4:
            uverbs = tags.pop(1)
            tags.insert(3,uverbs)



    out_dict = get_out_dict(i, vocab_sound_files[i])
    if i==0:
        out_dict['skip_on_semicolon'] = False
        out_dict['sound_silence_threshold'] = 1000
    # if i==2:
    #     out_dict['skip_on_beginning'] = 1
    #     out_dict['skip_on_semicolon'] = False
    if i==3:
        out_dict['sound_silence_threshold'] = 300

    words_sum = 0
    for t in tags:
        tag = t[0]
        cat = { 'category': tag, 'vocabulary': []}
        vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
        subtags = get_subtags(vocs, tag)
        if i in [0,1] or len(subtags) in [0,1]:
            cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in vocs]
            apply_hacks(cat, i, tag)
        else:
            scats = []
            for stag in subtags:
                stag = stag[0]
                scat = { 'category': stag, 'vocabulary': []}
                svocs = list(filter(lambda x: stag in x['tags'], vocs))
                scat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in svocs]
                apply_hacks(scat, i, tag, stag)
                scats.append(scat)
            cat['vocabulary'] = scats

        out_dict['cards'].append(cat)
        words_sum = words_sum + len(cat['vocabulary'])
    print(f'saving K{i+1}: {words_sum} words')

    folder_path = f'utils/script_output/L{str(i+1).zfill(2)}'
    os.makedirs(folder_path, exist_ok=True)

    with open(f'{folder_path}/01_vocabulary.yaml', 'w+') as o:
        yaml.dump(out_dict, o)

## 00 greetings
vocab_1 = vocab[0]
tag_vocab = list(filter(lambda x: any([y == 'L1_Greetings' for y in x['tags']]), vocab_1))
tags = [tuple(filter(lambda e: not e.endswith('Vocabulary'), x['tags'])) for x in tag_vocab]
tags = unique(tags)
tags = list(filter(lambda x: len(x) == 1, tags))
out_dict = get_out_dict(-1, 'Kaiwa_Bunpo_L00/K00_01.mp3', 0)
out_dict['skip_on_beginning'] = 0
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    if len(subtags) in [0,1]:
        cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in vocs]
        for v in cat['vocabulary']:
            if v['japanese'] == 'いいえ。':
                v['skip_on_semicolon'] = False
    else:
        scats = []
        for stag in subtags:
            stag = stag[0]
            scat = { 'category': stag, 'vocabulary': []}
            svocs = list(filter(lambda x: stag in x['tags'], vocs))
            scat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in svocs]
            apply_hacks(scat, i, tag, stag)
            scats.append(scat)
        cat['vocabulary'] = scats

    out_dict['cards'].append(cat)
os.makedirs('utils/script_output/L00', exist_ok=True)

with open('utils/script_output/L00/01_greetings.yaml', 'w+') as o:
    yaml.dump(out_dict, o)



## 00 numbers
vocab_1 = vocab[0]
tag_vocab = list(filter(lambda x: any([y == 'L1_Numbers' for y in x['tags']]), vocab_1))
tags = [tuple(['L1_Numbers'])]
out_dict = get_out_dict(-1, 'Kaiwa_Bunpo_L00/K00_02.mp3', 1)
out_dict['skip_on_beginning'] = 0
out_dict['only_japanese'] = 1
out_dict['sound_silence_threshold'] = 400
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': num2kanji(v['eng'])} for v in vocs]
    for v in cat['vocabulary']:
        if '／' in v['japanese']:
            v['fuse_with_next'] = v['japanese'].count('／')
        if v['kanji'] is None:
            del v['kanji']
    apply_hacks(cat, i, tag)
    out_dict['cards'].append(cat)

with open('utils/script_output/L00/02_numbers_0-100.yaml', 'w+') as o:
    yaml.dump(out_dict, o)



## 01 additional vocab
vocab_1 = vocab[0]
tag_vocab = list(filter(lambda x: any([y.endswith('Additional_Vocabulary') for y in x['tags']]), vocab_1))
tags = [tuple(filter(lambda e: not e.endswith('Vocabulary'), x['tags'])) for x in tag_vocab]
tags = unique(tags)
tags = list(filter(lambda x: len(x) == 1, tags))
out_dict = get_out_dict(0, 'Kaiwa_Bunpo_L01/K01_07.mp3', 1)
out_dict['skip_on_beginning'] = 1
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    if len(subtags) in [0,1]:
        cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in vocs]
        apply_hacks(cat, i, tag)
    else:
        scats = []
        for stag in subtags:
            stag = stag[0]
            scat = { 'category': stag, 'vocabulary': []}
            svocs = list(filter(lambda x: stag in x['tags'], vocs))
            scat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in svocs]
            apply_hacks(scat, i, tag, stag)
            scats.append(scat)
        cat['vocabulary'] = scats

    out_dict['cards'].append(cat)

with open('utils/script_output/L01/02_additional_vocabulary.yaml', 'w+') as o:
    yaml.dump(out_dict, o)



## 02 numbers2
vocab_1 = vocab[1]
tag_vocab = list(filter(lambda x: any([y == 'Numbers' for y in x['tags']]), vocab_1))
tags = [tuple(['Numbers'])]
out_dict = get_out_dict(1, 'Kaiwa_Bunpo_L02/K02_07.mp3', 1)
out_dict['skip_on_beginning'] = 3
out_dict['only_japanese'] = 1
out_dict['sound_silence_threshold'] = 400
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': num2kanji(v['eng'])} for v in vocs]
    cat['vocabulary'].insert(0, {'japanese': 'ひゃく', 'english': '100', 'kanji': num2kanji('100')})
    for v in cat['vocabulary']:
        if 'っ' in v['japanese'] or 'び' in v['japanese'] or 'ぜ' in v['japanese'] or v['japanese'] == 'いちまん':
            v['japanese'] += '*'

    apply_hacks(cat, i, tag)
    out_dict['cards'].append(cat)

with open('utils/script_output/L02/02_numbers_100-90000.yaml', 'w+') as o:
    yaml.dump(out_dict, o)

## 02 usefull_expressions
# vocab_1 = vocab[1]
# tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
# tags = [tuple(['Useful_Expressions'])]
# out_dict = get_out_dict(1, None, 2)
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     subtags = get_subtags(vocs, tag)
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng']} for v in vocs]
#     apply_hacks(cat, i, tag)
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L02/03_Useful_Expressions.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)


# manually changed output
# ## 04 time words
# vocab_1 = vocab[3]
# tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
# tags = [tuple(['Useful_Expressions'])]
# out_dict = get_out_dict(3, None, 4)
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     subtags = get_subtags(vocs, tag)
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
#     apply_hacks(cat, i, tag)
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L04/04_Time_Words.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)

# manually changed output
## 026usefull_expressions
# vocab_1 = vocab[5]
# tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
# tags = [tuple(['Useful_Expressions'])]
# out_dict = get_out_dict(5, None, 1)
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     subtags = get_subtags(vocs, tag)
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng']} for v in vocs]
#     apply_hacks(cat, i, tag)
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L06/02_Useful_Expressions.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)

# todo: add kinship terms

# 07 usefull_expressions
vocab_1 = vocab[6]
tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
tags = [tuple(['Useful_Expressions'])]
out_dict = get_out_dict(6, None, 2)
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
    apply_hacks(cat, i, tag)
    out_dict['cards'].append(cat)

with open('utils/script_output/L07/03_bodyparts.yaml', 'w+') as o:
    yaml.dump(out_dict, o)


# # 09 usefull_expressions
# vocab_1 = vocab[8]
# tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
# tags = [tuple(['Useful_Expressions'])]
# out_dict = get_out_dict(8, None, 1)
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     subtags = get_subtags(vocs, tag)
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
#     apply_hacks(cat, i, tag)
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L09/02_colors.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)

# 10 usefull_expressions
vocab_1 = vocab[9]
tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
tags = [tuple(['Useful_Expressions'])]
out_dict = get_out_dict(9, None, 1)
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
    apply_hacks(cat, i, tag)
    out_dict['cards'].append(cat)

with open('utils/script_output/L10/02_train_station.yaml', 'w+') as o:
    yaml.dump(out_dict, o)

## 11 additional vocab
# vocab_1 = vocab[10]
# tag_vocab = list(filter(lambda x: any([y.endswith('Additional_Vocabulary') for y in x['tags']]), vocab_1))
# tags = [tuple(filter(lambda e: not e.endswith('Vocabulary'), x['tags'])) for x in tag_vocab]
# tags = unique(tags)
# tags = list(filter(lambda x: len(x) == 1, tags))
# out_dict = get_out_dict(0, 'Kaiwa_Bunpo_L11/K11_09.mp3', 1)
# out_dict['skip_on_beginning'] = 1
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanji': v['kan']} for v in vocs]
#     cat['vocabulary'].insert(0, {'japanese': 'しょくぎょう', 'english': 'Occupations', 'kanji': '職業'})
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L11/02_additional_vocabulary.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)


# 11 usefull_expressions
# vocab_1 = vocab[10]
# tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
# tags = [tuple(['Useful_Expressions'])]
# out_dict = get_out_dict(10, None, 2)
# for t in tags:
#     tag = t[0]
#     cat = { 'category': tag, 'vocabulary': []}
#     vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
#     subtags = get_subtags(vocs, tag)
#     cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
#     apply_hacks(cat, i, tag)
#     out_dict['cards'].append(cat)

# with open('utils/script_output/L11/03_japanese_class.yaml', 'w+') as o:
#     yaml.dump(out_dict, o)

# 12 usefull_expressions
vocab_1 = vocab[11]
tag_vocab = list(filter(lambda x: any([y == 'Useful_Expressions' for y in x['tags']]), vocab_1))
tags = [tuple(['Useful_Expressions'])]
out_dict = get_out_dict(11, None, 1)
for t in tags:
    tag = t[0]
    cat = { 'category': tag, 'vocabulary': []}
    vocs = list(filter(lambda x: tag in x['tags'], tag_vocab))
    subtags = get_subtags(vocs, tag)
    cat['vocabulary'] = [{'japanese': v['jap'], 'english': v['eng'], 'kanjis': v['kan']} for v in vocs]
    apply_hacks(cat, i, tag)
    out_dict['cards'].append(cat)

with open('utils/script_output/L12/02_health_and_illness.yaml', 'w+') as o:
    yaml.dump(out_dict, o)