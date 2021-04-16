import json
import urllib.request
import pprint
pp = pprint.PrettyPrinter(indent=2)
from ruamel.yaml import YAML
yaml=YAML()



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

def get_kanji_data():
    result = invoke('deckNamesAndIds')
    result = list(filter(lambda v: v[0].startswith('G-Anki::Volume 1::'), result.items()))
    kanjis = []
    for i in range(1, 3):
        cards = invoke('findNotes', query=f'"deck:G-Anki::Volume 1::G-Anki Lesson {str(i).zfill(2)}"')
        card = invoke('notesInfo', notes=cards)
        current_kanjis = {}
        for e in card:
            fields = e['fields']
            if 'Kanji' in fields and 'Kana Reading' in fields:
                current_kanjis[fields['Kana Reading']['value']] = fields['Kanji']['value']
        
        kanjis.append(current_kanjis)
    for i, d in enumerate(kanjis):
        with open(f'utils/script_output/kanji_data_{str(i+1).zfill(2)}.yaml', 'w+') as o:
            yaml.dump(d, o)
    return kanjis

