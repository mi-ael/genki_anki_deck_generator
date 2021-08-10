from typing import Tuple
import requests
import json

def fetch_kanjis(kana: str):
    print(f"fetching kanji for {kana} from jisho.org")
    answer = requests.get('https://jisho.org/api/v1/search/words', params={"keyword": kana})
    parsed = json.loads(answer.text)
    data = parsed["data"]
    if len(data) > 0:
        japanese = data[0]["japanese"]
        if len(japanese) > 0:
            if "word" in japanese[0].keys():
                return japanese[0]["word"]
    print(f"could not fetch kanji for {kana}")
    return ""

kanji_dict = None

def fetch_kanji_meanings(kanji: str) -> Tuple[str, bool]:
    global kanji_dict
    if kanji_dict is None:
        answer = requests.get('https://raw.githubusercontent.com/davidluzgouveia/kanji-data/master/kanji-wanikani.json')
        parsed = json.loads(answer.text)
        kanji_dict = {k:v["wk_meanings"][0] for k,v in parsed.items()}
    if kanji not in kanji_dict.keys():
        #print(f"unknown kanji: {kanji} ")
        #return "[unknown kanji]"
        return kanji, False
    return kanji_dict[kanji], True
