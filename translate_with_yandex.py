import os as os
import json as json
import requests as requests

def f_translate(textToTranslate, lang = 'ru-en'):
    try:
        if 'TRANSLATOR_YANDEX_API_KEY' in os.environ: 
            apiKey = os.environ['TRANSLATOR_YANDEX_API_KEY']
        else: 
            raise Exception('Environment variable not set for yandex api key.')
        api_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        params = {
        "lang": lang,
        "text": textToTranslate,
        "key": apiKey,
        }
        response = requests.post(api_url, data=params)
        return(response.json()['text'][0])
    except:
         return 'Oeps'

