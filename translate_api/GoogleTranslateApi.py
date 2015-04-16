#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import requests
import json
from HTMLParser  import HTMLParser

class Google_Translate(object):
    '''
    English            : en
    Chinese Simplified : zh-CN
    '''
    
    def __init__(self):
        self.baseUrl = "https://www.googleapis.com/language/translate/v2"
        self.FORMATS = ('text', 'html')
        self.params = {}
        
    def setParams(self, key, source_lang, target_lang, trans_text, format = 'text'):
        ''' set query parameters
            key          --the api key (required)
            source_lang  --source language  (optional)
            target_lang  --target language  (required)
            trans_text         --translate text and text may be either a string or a list of strings(required)
            format       -- optional'''
        
        text_parser = HTMLParser()
        text = text_parser.unescape(trans_text)
        if format not in self.FORMATS:
            raise TypeError('The format should be one of %s' % (self.FORMATS))
        
        params = {'key': key,
                  'source': source_lang,
                  'target': target_lang,
                  'q': text,
                  'format': format}
        self.params.update(params)
    
    def translate(self):
        url = self.baseUrl
        try:
            r = requests.get(url, params = self.params, timeout = 100)
        except Exception:
            return 'timeout'
        if r.ok:
            result_var = json.loads(r.text)
            result = result_var['data']['translations'][0]['translatedText']
            return result
        else:
            raise Exception(r.status_code)
        