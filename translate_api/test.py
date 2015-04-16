#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from GoogleTranslateApi import Google_Translate
import setting
import urllib

if __name__=='__main__':
    text="Refurbished: Acer 2955U &#40;1.40GHz&#41; 16GB SSD 11.6&#34; Chrome OS"
    trans_test = Google_Translate()
    trans_test.setParams(setting.api_key, 'en', 'zh-CN', text)
    print trans_test.translate()