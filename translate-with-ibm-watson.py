# https://cloud.ibm.com/apidocs/language-translator?code=python#translate
# https://www.makeuseof.com/tag/json-python-parsing-simple-guide/

from ibm_watson import LanguageTranslatorV3
from ibm_watson import ApiException
import json as json
import pathlib as pathlib
import os as os
import pandas as pd

modelId = 'ru-en'
#filePath = pathlib.Path(pathlib.dirname(__file__) if "__file__" in locals() else os.getcwd())
fileName = 'item_categories.csv'
variableName = 'item_category_name'

df = pd.read_csv(pathlib.Path(os.getcwd(), 'input',fileName))
df.count()

def f_translate(textToTranslate, modelId = 'nl-en'):
    try:
        if 'TRANSLATOR_WATSON_API_KEY' in os.environ: 
            apiKey = os.environ['TRANSLATOR_WATSON_API_KEY']
        else: 
            raise Exception('Environment variable not set for watson api key.')
        version = '2018-05-01'
        apiURL = 'https://gateway-fra.watsonplatform.net/language-translator/api'
        language_translator = LanguageTranslatorV3(
            version=version,
            iam_apikey=apiKey,
            url=apiURL
        )
        language_translator.set_url(apiURL)
        translation = language_translator.translate(
            text=textToTranslate,
            model_id=modelId).get_result()
        obj = json.loads(json.dumps(translation, indent=2, ensure_ascii=False))
        textTranslation = obj['translations'][0]['translation']
        return(textTranslation)
    except ApiException as ex:
        return("Method failed with status code " + str(ex.code) + ": " + ex.message)

def f_translate_df(df, variableName, modelId = 'nl-en'):
    df[variableName] = df[variableName].apply(lambda x: f_translate(x, modelId))
    return(df)

df = f_translate_df(df, variableName, modelId)

fileName = fileName.replace('.csv','') + '_translated.csv'

df.to_csv(pathlib.Path(os.getcwd(), 'output',fileName),sep = ',',index=False, header=True)
df.count()
